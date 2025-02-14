from collections import defaultdict
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

import tiktoken

from intric.ai_models.completion_models.completion_model import Context, Message
from intric.ai_models.completion_models.static_prompts import (
    HALLUCINATION_GUARD,
    SHOW_REFERENCES_PROMPT,
    TRANSCRIPTION_PROMPT,
)
from intric.files.file_models import File, FileType
from intric.main.exceptions import QueryException
from intric.sessions.session import SessionInDB

if TYPE_CHECKING:
    from uuid import UUID

    from intric.info_blobs.info_blob import InfoBlobChunkInDBWithScore

CONTEXT_SIZE_BUFFER = 1000  # Counting tokens is not an exakt science, leave some buffer
MIN_PERCENTAGE_KNOWLEDGE = (
    0.8  # Strive towards a minimum of 80% of the context as knowledge
)


def count_tokens(text: str):
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def _build_files_string(files: list[File]):
    if files:
        files_string = "\n".join(
            f'{{"filename": "{file.name}", "text": "{file.text}"}}' for file in files
        )

        return (
            "Below are files uploaded by the user. "
            "You should act like you can see the files themselves, "
            "and in no way whatsoever reveal the specific formatting "
            "you see below:"
            f"\n\n{files_string}"
        )

    return ""


@dataclass
class ChunkGrouping:
    info_blob_id: "UUID"
    info_blob_title: str
    start_chunk: int
    end_chunk: int
    text: str
    chunk_count: int
    relevance_score: Optional[float] = None


class _Prompt:
    def __init__(self):
        self.prompt = None
        self.knowledge = None
        self.attachments = None
        self._knowledge_tokens = 0

    def __str__(self):
        return f"{self.prompt}\n\n{self.knowledge}\n\n{self.attachments}".strip()

    @staticmethod
    def _common_overlap(text1: str, text2: str):
        # Cache the text lengths to prevent multiple calls.
        text1_length = len(text1)
        text2_length = len(text2)
        # Eliminate the null case.
        if text1_length == 0 or text2_length == 0:
            return 0
        # Truncate the longer string.
        if text1_length > text2_length:
            text1 = text1[-text2_length:]
        elif text1_length < text2_length:
            text2 = text2[:text1_length]
        # Quick check for the worst case.
        if text1 == text2:
            return min(text1_length, text2_length)

        # Start by looking for a single character match
        # and increase length until no match is found.
        best = 0
        length = 1
        while True:
            pattern = text1[-length:]
            found = text2.find(pattern)
            if found == -1:
                return best
            length += found
            if text1[-length:] == text2[:length]:
                best = length
                length += 1

    def _join_overlapping_text(self, chunks: list["InfoBlobChunkInDBWithScore"]):
        if not chunks:
            return ""

        result_string = chunks[0].text

        for i in range(1, len(chunks)):
            prev_chunk = chunks[i - 1].text
            current_chunk = chunks[i].text

            overlap = self._common_overlap(prev_chunk, current_chunk)

            result_string = f"{result_string}{current_chunk[overlap:]}"

        return result_string

    def _reconstruct_and_order_chunks(
        self,
        chunks: list["InfoBlobChunkInDBWithScore"],
        max_tokens: int,
        version: int,
    ):
        # Create a dictionary to store chunk indices
        chunk_indices = {id(chunk): i for i, chunk in enumerate(chunks)}

        # Group chunks by info_blob
        chunks_by_info_blob = {}
        used_tokens = 0
        for chunk in chunks:
            chunk_tokens = count_tokens(chunk.text)

            if chunks_by_info_blob.get(chunk.info_blob_id) is None:
                chunks_by_info_blob[chunk.info_blob_id] = []

                # Count the tokens for the metadata
                chunk_tokens += count_tokens(
                    '"""source_title: {}, source_id: {}\n"""'.format(
                        chunk.info_blob_title, str(chunk.info_blob_id)[:8]
                    )
                )

            if chunk_tokens + used_tokens > max_tokens:
                break

            chunks_by_info_blob[chunk.info_blob_id].append(chunk)
            used_tokens += chunk_tokens

        # Save the used_tokens for later
        self._knowledge_tokens = used_tokens

        # Process each document
        chunk_groupings = []
        grouping_scores = defaultdict(float)

        for doc_id, doc_chunks in chunks_by_info_blob.items():
            # Edgecase if the first chunk of a new info-blob is the cutoff point
            if not doc_chunks:
                continue

            # Sort chunks by their order in the original document
            doc_chunks.sort(key=lambda x: x.chunk_no)

            # Group coherent chunks
            coherent_groups = []
            current_group = [doc_chunks[0]]

            for i in range(1, len(doc_chunks)):
                if doc_chunks[i].chunk_no == current_group[-1].chunk_no + 1:
                    current_group.append(doc_chunks[i])
                else:
                    coherent_groups.append(current_group)
                    current_group = [doc_chunks[i]]

            coherent_groups.append(current_group)

            # Process each coherent group as a separate document
            for group in coherent_groups:
                full_text = self._join_overlapping_text(group)

                chunk_grouping = ChunkGrouping(
                    info_blob_id=doc_id,
                    info_blob_title=group[0].info_blob_title,
                    start_chunk=group[0].chunk_no,
                    end_chunk=group[-1].chunk_no,
                    text=full_text,
                    chunk_count=len(group),
                )

                # Calculate score based on the position of chunks in the original input
                score = sum(1 / (chunk_indices[id(chunk)] + 1) for chunk in group)
                grouping_scores[id(chunk_grouping)] = score

                chunk_groupings.append(chunk_grouping)

        # Add scores to documents and sort by score
        for grouping in chunk_groupings:
            grouping.relevance_score = grouping_scores[id(grouping)]

        chunk_groupings.sort(key=lambda x: x.relevance_score, reverse=True)

        if version == 1:
            return "\n".join(
                f'"""{chunk_grouping.text}"""' for chunk_grouping in chunk_groupings
            )

        elif version == 2:
            return "\n".join(
                '"""source_title: {}, source_id: {}\n{}"""'.format(
                    chunk_grouping.info_blob_title,
                    str(chunk_grouping.info_blob_id)[:8],
                    chunk_grouping.text,
                )
                for chunk_grouping in chunk_groupings
            )

    @property
    def num_tokens(self):
        _tokens = 0

        if self.prompt:
            _tokens += count_tokens(self.prompt)

        if self.knowledge:
            _tokens += self._knowledge_tokens

        if self.attachments:
            _tokens += count_tokens(self.attachments)

        return _tokens

    def add_prompt(self, prompt: str, transcription: bool):
        if transcription:
            prompt = f"{TRANSCRIPTION_PROMPT}\n{prompt}"

        self.prompt = prompt

    def add_knowledge(
        self, chunks: list["InfoBlobChunkInDBWithScore"], max_tokens: int, version: int
    ):
        if version == 1:
            before_knowledge_prompt = HALLUCINATION_GUARD
        elif version == 2:
            before_knowledge_prompt = SHOW_REFERENCES_PROMPT

        before_knowledge_prompt_tokens = count_tokens(before_knowledge_prompt)
        chunk_text = self._reconstruct_and_order_chunks(
            chunks=chunks,
            max_tokens=max_tokens - before_knowledge_prompt_tokens,
            version=version,
        )

        # If the limits result in no knowledge at all
        if not chunk_text:
            self.knowledge = ""

        else:
            self.knowledge = f"{before_knowledge_prompt}\n\n{chunk_text}"

    def add_attachments(self, files: list[File]):
        self.attachments = _build_files_string(files=files)

    def get_tokens_of_knowledge(self):
        return self._knowledge_tokens


class ContextBuilder:
    def _build_input(
        self,
        input_str: str,
        files: list[File] = [],
        transcription_inputs: list[str] = [],
    ):
        if files:
            files_string = _build_files_string(files)
            input_str = f"{files_string}\n\n{input_str}"

        if transcription_inputs:
            # For now, transcription is only available for apps,
            # which means that we don't have to worry about what
            # happens with follow-up questions.
            transcription_string = "\n".join(
                map(lambda t: f"transcription: \"\"{t}\"\"", transcription_inputs)
            )
            input_str = f"{transcription_string}\n\n{input_str}"

        return input_str.strip()

    @staticmethod
    def _get_files_by_type(files: list[File], file_type: FileType):
        return [file for file in files if file.file_type == file_type]

    def _build_messages(
        self, session: Optional[SessionInDB], max_tokens: int, min_len: int = 3
    ):
        if session is None:
            return [], 0

        messages = []
        total_tokens = 0

        for message in reversed(session.questions):
            question = self._build_input(
                message.question,
                self._get_files_by_type(message.files, FileType.TEXT),
            )
            answer = message.answer
            images = self._get_files_by_type(message.files, FileType.IMAGE)

            message_tokens = count_tokens(question) + count_tokens(answer)

            if len(messages) > min_len and total_tokens + message_tokens > max_tokens:
                break

            messages.insert(
                0,
                Message(
                    question=question,
                    answer=answer,
                    images=images,
                ),
            )

            total_tokens += message_tokens

        return messages, total_tokens

    def build_context(
        self,
        input_str: str,
        *,
        max_tokens: int,
        files: list[File] = [],
        prompt: str = "",
        prompt_files: list[File] = [],
        transcription_inputs: list[str] = [],
        info_blob_chunks: list["InfoBlobChunkInDBWithScore"] = [],
        session: Optional[SessionInDB] = None,
        version: int = 1,
    ):
        tokens_used = 0
        max_tokens_usable = max_tokens - CONTEXT_SIZE_BUFFER  # Leave some room.

        # Create the input, count the tokens.
        _input_string = self._build_input(
            input_str=input_str,
            files=self._get_files_by_type(files, FileType.TEXT),
            transcription_inputs=transcription_inputs,
        )
        tokens_used_input = count_tokens(_input_string)
        tokens_used += tokens_used_input

        # Create the necessary parts of the prompt.
        # Add the tokens used.
        _prompt = _Prompt()
        _prompt.add_prompt(prompt=prompt, transcription=bool(transcription_inputs))
        _prompt.add_attachments(
            files=self._get_files_by_type(prompt_files, FileType.TEXT)
        )
        tokens_used += _prompt.num_tokens

        # Create the messages, keeping within the 80% mark,
        # and minimum 3.
        max_tokens_messages = (
            int(max_tokens_usable * (1 - MIN_PERCENTAGE_KNOWLEDGE)) - tokens_used
        )
        messages, tokens_used_messages = self._build_messages(
            session=session, max_tokens=max_tokens_messages, min_len=3
        )
        tokens_used += tokens_used_messages

        # Check for worst case.
        # Up until this point, all text will be
        # assumed by the user to be there,
        # and erroring is preferable to not
        # including something.
        if tokens_used > max_tokens_usable:
            raise QueryException("Query too long")

        # Add the knowledge in all the space that is left.
        tokens_left = max_tokens_usable - tokens_used
        _prompt.add_knowledge(
            chunks=info_blob_chunks, max_tokens=tokens_left, version=version
        )
        prompt_text = str(_prompt)
        tokens_used += _prompt.get_tokens_of_knowledge()

        return Context(
            input=_input_string,
            prompt=prompt_text,
            messages=messages,
            images=self._get_files_by_type(files, FileType.IMAGE),
            token_count=tokens_used,
        )
