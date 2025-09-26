# import whisper
# from .config import MODEL_SIZE
# from .utils import save_srt
# import os

# class AudioTranscriber:
#     def __init__(self):
#         print(f"[+] Loading Whisper model: {MODEL_SIZE}")
#         self.model = whisper.load_model(MODEL_SIZE)

#     def transcribe_audio(self, audio_path, captions_dir):
#         """Transcribe audio file and save captions as SRT"""
#         print(f"[+] Transcribing: {audio_path}")
#         result = self.model.transcribe(audio_path, task="transcribe")

#         # Save captions as SRT
#         filename = os.path.basename(audio_path)
#         save_srt(result["text"], filename, captions_dir)

import whisper
from .utils import save_transcript, save_srt

class Transcriber:
    def __init__(self, model_name="base"):
        self.model = whisper.load_model(model_name)

    
    def transcribe_audio(self, file_path, language="en"):
        """Full transcript + segments with timestamps"""
        result = self.model.transcribe(file_path, language=language, task="transcribe")
        return result
    
    def get_segments(self, file_path, language="en"):
        result = self.model.transcribe(file_path, language=language, task="transcribe")
        return result.get("segments", [])

    # def transcribe(self, audio_path: str, out_dir="captions"):
    #     result = self.model.transcribe(audio_path, task="transcribe")

    #     transcript_path = f"{out_dir}/transcript.txt"
    #     srt_path = f"{out_dir}/captions.srt"

    #     save_transcript(result["text"], transcript_path)
    #     save_srt(result["segments"], srt_path)

    #     return result, transcript_path, srt_path
