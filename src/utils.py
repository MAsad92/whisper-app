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
import re

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

def highlight_keywords(text, keywords):
    """Highlight keywords in transcript using Markdown bold style."""
    if not keywords:
        return text
    regex = re.compile(r"\b(" + "|".join(map(re.escape, keywords)) + r")\b", re.IGNORECASE)
    return regex.sub(r"**\1**", text)

def format_transcript(text, max_sentences=3):
    """
    Split transcript into paragraphs with line breaks after a few sentences.
    """
    import re
    # Split by sentence endings (.?!)
    sentences = re.split(r'(?<=[.!?]) +', text)
    
    # Group into chunks
    paragraphs = []
    for i in range(0, len(sentences), max_sentences):
        chunk = " ".join(sentences[i:i+max_sentences])
        paragraphs.append(chunk.strip())
    
    # Join with double line breaks
    return "\n\n".join(paragraphs)    