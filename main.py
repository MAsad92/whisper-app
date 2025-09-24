import streamlit as st
import whisper
import tempfile

# Load model once
@st.cache_resource
def load_model():
    return whisper.load_model("small")

model = load_model()

st.title("🎙️ Audio to Captions (Whisper)")
st.write("Upload an audio file and get transcriptions with captions.")

uploaded_file = st.file_uploader("Upload audio", type=["mp3", "wav", "m4a", "flac"])

if uploaded_file is not None:
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(uploaded_file.read())
        audio_path = tmp.name

    st.info("Transcribing... please wait ⏳")
    result = model.transcribe(audio_path, task="transcribe")

    st.subheader("Transcription")
    st.text(result["text"])

    # Save captions to .srt
    srt_file = audio_path.replace(".mp3", ".srt")
    with open(srt_file, "w", encoding="utf-8") as f:
        f.write(result["text"])

    st.success("✅ Transcription done!")
    st.download_button("Download Captions (SRT)", result["text"], file_name="captions.srt")
