import os

def get_audio_files(audio_dir):
    """Return list of audio files in the given directory"""
    supported_formats = (".mp3", ".wav", ".m4a", ".flac")
    return [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith(supported_formats)]

def save_srt(text, filename, captions_dir):
    """Save transcription text as .srt file"""
    output_path = os.path.join(captions_dir, filename.replace(".mp3", ".srt").replace(".wav", ".srt"))
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"[+] Captions saved to {output_path}")
