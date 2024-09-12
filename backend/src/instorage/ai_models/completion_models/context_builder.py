from typing import Optional

from instorage.ai_models.completion_models.completion_model import Context, Message
from instorage.ai_models.completion_models.guardrails import (
    FAIRNESS_GUARD,
    HALLUCINATION_GUARD,
)
from instorage.files.file_models import File, FileType
from instorage.info_blobs.info_blob import InfoBlobChunkInDBWithScore
from instorage.sessions.session import SessionInDB


class ContextBuilder:

    @staticmethod
    def _build_input(input: str, files: list[File]):
        if files:
            files_string = "\n".join(
                f'{{"filename": "{file.name}", "text": "{file.text}"}}'
                for file in files
            )
            input = (
                "Below are files uploaded by the user. "
                "You should act like you can see the files themselves:"
                f"\n\n{files_string}"
                f"\n\n{input}"
            )

        return input.strip()

    @staticmethod
    def _build_prompt(
        prompt: str = "",
        info_blob_chunks: list[InfoBlobChunkInDBWithScore] = [],
        fairness_guard: bool = False,
        hallucination_guard: bool = False,
    ):
        if prompt:
            prompt = f"{prompt}\n\n"

        if fairness_guard:
            prompt = f"{prompt}{FAIRNESS_GUARD}\n\n"

        if hallucination_guard:
            prompt = f"{prompt}{HALLUCINATION_GUARD}\n\n"

        if info_blob_chunks:
            chunks = "\n".join(f'"""{chunk.text}"""' for chunk in info_blob_chunks)
            prompt = f"{prompt}{chunks}"

        return prompt.strip()

    @staticmethod
    def _get_files_by_type(files: list[File], file_type: FileType):
        return [file for file in files if file.file_type == file_type]

    def _build_messages(self, session: Optional[SessionInDB]):
        if session is None:
            return []

        return [
            Message(
                question=self._build_input(
                    message.question,
                    self._get_files_by_type(message.files, FileType.TEXT),
                ),
                answer=message.answer,
                images=self._get_files_by_type(message.files, FileType.IMAGE),
            )
            for message in session.questions
        ]

    def build_context(
        self,
        input: str,
        files: list[File] = [],
        prompt: str = "",
        info_blob_chunks: list[InfoBlobChunkInDBWithScore] = [],
        fairness_guard: bool = False,
        hallucination_guard: bool = False,
        session: Optional[SessionInDB] = None,
    ):
        input = self._build_input(
            input=input, files=self._get_files_by_type(files, FileType.TEXT)
        )
        prompt = self._build_prompt(
            prompt=prompt,
            info_blob_chunks=info_blob_chunks,
            fairness_guard=fairness_guard,
            hallucination_guard=hallucination_guard,
        )
        messages = self._build_messages(session=session)

        return Context(
            input=input,
            prompt=prompt,
            messages=messages,
            images=self._get_files_by_type(files, FileType.IMAGE),
        )
