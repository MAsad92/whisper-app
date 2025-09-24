import whisper
from .config import MODEL_SIZE
from .utils import save_srt
import os

class AudioTranscriber:
    def __init__(self):
        print(f"[+] Loading Whisper model: {MODEL_SIZE}")
        self.model = whisper.load_model(MODEL_SIZE)

    def transcribe_audio(self, audio_path, captions_dir):
        """Transcribe audio file and save captions as SRT"""
        print(f"[+] Transcribing: {audio_path}")
        result = self.model.transcribe(audio_path, task="transcribe")

        # Save captions as SRT
        filename = os.path.basename(audio_path)
        save_srt(result["text"], filename, captions_dir)