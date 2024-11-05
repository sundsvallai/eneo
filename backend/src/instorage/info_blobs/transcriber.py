# Copyright (c) 2024 Sundsvalls Kommun
#
# Licensed under the MIT License.

from pathlib import Path

from instorage.ai_models.transcription_models.model_adapters.whisper import (
    OpenAISTTModelAdapter,
)
from instorage.files import audio


class Transcriber:
    def __init__(self, adapter: OpenAISTTModelAdapter):
        self.adapter = adapter

    async def transcribe(self, *, filepath: Path):
        async with audio.to_wav(filepath) as wav_file:
            return await self.adapter.get_text_from_file(wav_file)
