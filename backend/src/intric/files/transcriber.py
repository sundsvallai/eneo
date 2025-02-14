# MIT License

import tempfile
from pathlib import Path

from intric.ai_models.transcription_models.model_adapters.whisper import (
    OpenAISTTModelAdapter,
)
from intric.files import audio
from intric.files.audio import AudioMimeTypes
from intric.files.file_models import File


class Transcriber:
    def __init__(self, adapter: OpenAISTTModelAdapter):
        self.adapter = adapter

    async def transcribe(self, file: File):
        if file.blob is None or not AudioMimeTypes.has_value(file.mimetype):
            raise ValueError("File needs to be an audio file")

        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                temp_file.write(file.blob)
                temp_file_path = Path(temp_file.name)

            result = await self.transcribe_from_filepath(filepath=temp_file_path)
        finally:
            temp_file_path.unlink()  # Clean up the temporary file

        return result

    async def transcribe_from_filepath(self, *, filepath: Path):
        async with audio.to_wav(filepath) as wav_file:
            return await self.adapter.get_text_from_file(wav_file)
