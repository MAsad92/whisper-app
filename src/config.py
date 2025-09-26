import os

# Model configuration: "tiny", "base", "small", "medium", "large"
MODEL_SIZE = "small" #small

# Directories
AUDIO_DIR = os.path.join(os.getcwd(), "audio")
CAPTIONS_DIR = os.path.join(os.getcwd(), "captions")

# Ensure output directory exists
os.makedirs(CAPTIONS_DIR, exist_ok=True)

# config.py
SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "hi": "Hindi"
}

DEFAULT_LANGUAGE = "en"
