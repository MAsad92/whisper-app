# import streamlit as st
# import whisper
# import tempfile

# # Load model once
# @st.cache_resource
# def load_model():
#     return whisper.load_model("small")

# model = load_model()

# st.title("🎙️ Audio to Captions (Whisper)")
# st.write("Upload an audio file and get transcriptions with captions.")

# uploaded_file = st.file_uploader("Upload audio", type=["mp3", "wav", "m4a", "flac"])

# if uploaded_file is not None:
#     # Save to temp file
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
#         tmp.write(uploaded_file.read())
#         audio_path = tmp.name

#     st.info("Transcribing... please wait ⏳")
#     result = model.transcribe(audio_path, task="transcribe")

#     st.subheader("Transcription")
#     st.text(result["text"])

#     # Save captions to .srt
#     srt_file = audio_path.replace(".mp3", ".srt")
#     with open(srt_file, "w", encoding="utf-8") as f:
#         f.write(result["text"])

#     st.success("✅ Transcription done!")
#     st.download_button("Download Captions (SRT)", result["text"], file_name="captions.srt")

import streamlit as st
import tempfile
import os
from src.transcriber import Transcriber

st.set_page_config(page_title="Audio to Captions", page_icon="🎙️", layout="wide")

st.title("🎙️ Audio Transcription & Caption Generator")
st.markdown("Upload an audio file to generate **transcripts** and **captions with timestamps (.srt)**.")

uploaded_file = st.file_uploader("Upload Audio", type=["mp3", "wav", "m4a"])

if uploaded_file is not None:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
        tmp_file.write(uploaded_file.read())
        audio_path = tmp_file.name

    st.info("⏳ Processing audio... Please wait.")

    transcriber = Transcriber(model_name="base")
    result, transcript_path, srt_path = transcriber.transcribe(audio_path, out_dir="captions")

    # Show transcript
    st.subheader("📝 Full Transcript")
    st.success(result["text"])

    # Show captions with timestamps in a nice format
    st.subheader("📺 Captions with Timestamps")
    for seg in result["segments"]:
        start = round(seg["start"], 2)
        end = round(seg["end"], 2)
        text = seg["text"]
        st.markdown(f"**[{start} → {end}]** {text}")

    # Download buttons
    st.subheader("⬇ Download Files")
    with open(transcript_path, "rb") as f:
        st.download_button("Download Transcript (.txt)", f, file_name="transcript.txt")

    with open(srt_path, "rb") as f:
        st.download_button("Download Captions (.srt)", f, file_name="captions.srt")
