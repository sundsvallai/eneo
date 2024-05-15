from dataclasses import dataclass
from typing import Optional

from instorage.ai_models.completion_models.guardrails import (
    FAIRNESS_GUARD,
    HALLUCINATION_GUARD,
)
from instorage.info_blobs.info_blob import InfoBlobChunkWithScore
from instorage.main.config import get_settings
from instorage.questions.question import QuestionInDB


@dataclass
class Context:
    input: str
    prompt: str
    background_info: str
    previous_questions: list[QuestionInDB]
    _document_chunks: list[str]


class ContextBuilder:
    def __init__(
        self,
        with_fairness_guard: bool = None,
        with_hallucination_guard: bool = None,
    ):
        self.with_fairness_guard = (
            with_fairness_guard if with_fairness_guard is not None else False
        )
        self.with_hallucination_guard = (
            with_hallucination_guard if with_hallucination_guard is not None else True
        )

        self._context = None

    def _create_prompt(self, prompt: Optional[str]):
        prompt = prompt or get_settings().instorage_default_prompt

        if self.with_fairness_guard:
            prompt = f"{prompt}\n\n{FAIRNESS_GUARD}"

        return prompt

    def _create_background_info(self, num: int = None):
        chunks_to_get = (
            self._context._document_chunks[:num]
            if int is not None
            else self._context._document_chunks
        )

        return "\n".join(chunks_to_get)

    def _create_document_chunks_list(
        self, document_chunks: Optional[list[InfoBlobChunkWithScore]]
    ):
        if not document_chunks:
            return []

        first_chunk = [
            (
                f"{HALLUCINATION_GUARD}\n\"\"\"{document_chunks[0].text}\"\"\""
                if self.with_hallucination_guard
                else f"\"\"\"{document_chunks[0].text}\"\"\""
            )
        ]
        rest_of_chunks = [f"\"\"\"{chunk.text}\"\"\"" for chunk in document_chunks[1:]]

        return first_chunk + rest_of_chunks

    def setup(
        self,
        input: str,
        prompt: str = None,
        document_chunks: list[InfoBlobChunkWithScore] = None,
        previous_questions: list[QuestionInDB] = None,
    ):
        self._context = Context(
            input=input,
            prompt=self._create_prompt(prompt),
            background_info=None,
            previous_questions=previous_questions or [],
            _document_chunks=self._create_document_chunks_list(document_chunks),
        )

    def get_prompt(self):
        return self._context.prompt

    def get_background_info(self, num: int = None):
        if num is not None or self._context.background_info is None:
            self._context.background_info = self._create_background_info(num)

        return self._context.background_info

    def get_input(self):
        return self._context.input

    def get_previous_questions(self, num: int = None):
        if num is not None:
            return self._context.previous_questions[-num:]

        return self._context.previous_questions

    def get_document_chunks_list(self):
        return self._context._document_chunks
