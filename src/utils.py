# import os

# def get_audio_files(audio_dir):
#     """Return list of audio files in the given directory"""
#     supported_formats = (".mp3", ".wav", ".m4a", ".flac")
#     return [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith(supported_formats)]

# def save_srt(text, filename, captions_dir):
#     """Save transcription text as .srt file"""
#     output_path = os.path.join(captions_dir, filename.replace(".mp3", ".srt").replace(".wav", ".srt"))
#     with open(output_path, "w", encoding="utf-8") as f:
#         f.write(text)
#     print(f"[+] Captions saved to {output_path}")

def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT hh:mm:ss,ms format."""
    h, r = divmod(int(seconds), 3600)
    m, s = divmod(r, 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def save_transcript(text: str, path: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def save_srt(segments, path: str):
    with open(path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, start=1):
            start = format_timestamp(seg["start"])
            end = format_timestamp(seg["end"])
            f.write(f"{i}\n{start} --> {end}\n{seg['text'].strip()}\n\n")
