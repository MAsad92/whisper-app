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

# import streamlit as st
# import tempfile
# import os
# from src.transcriber import Transcriber

# st.set_page_config(page_title="Audio to Captions", page_icon="🎙️", layout="wide")

# st.title("🎙️ Audio Transcription & Caption Generator")
# st.markdown("Upload an audio file to generate **transcripts** and **captions with timestamps (.srt)**.")

# uploaded_file = st.file_uploader("Upload Audio", type=["mp3", "wav", "m4a"])

# if uploaded_file is not None:
#     # Save uploaded file temporarily
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
#         tmp_file.write(uploaded_file.read())
#         audio_path = tmp_file.name

#     st.info("⏳ Processing audio... Please wait.")

#     transcriber = Transcriber(model_name="base")
#     result, transcript_path, srt_path = transcriber.transcribe(audio_path, out_dir="captions")

#     # Show transcript
#     st.subheader("📝 Full Transcript")
#     st.success(result["text"])

#     # Show captions with timestamps in a nice format
#     st.subheader("📺 Captions with Timestamps")
#     for seg in result["segments"]:
#         start = round(seg["start"], 2)
#         end = round(seg["end"], 2)
#         text = seg["text"]
#         st.markdown(f"**[{start} → {end}]** {text}")

#     # Download buttons
#     st.subheader("⬇ Download Files")
#     with open(transcript_path, "rb") as f:
#         st.download_button("Download Transcript (.txt)", f, file_name="transcript.txt")

#     with open(srt_path, "rb") as f:
#         st.download_button("Download Captions (.srt)", f, file_name="captions.srt")
import streamlit as st
import os
from src.transcriber import Transcriber
from src.utils import highlight_keywords
from src.config import SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="Audio to Captions",
    page_icon="🎙️",
    layout="wide"
)

# ----------------- CUSTOM CSS -----------------
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 2.2em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: gray;
        margin-bottom: 25px;
    }
    .transcript-box {
        background-color: #1a2b71;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #ddd;
        font-size: 1.05em;
        line-height: 1.6;
        color: white;
    }
    .timestamp {
        color: #4CAF50;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- HELPER FUNCTION -----------------
def format_transcript(text, max_words=25):
    """
    Break transcript text into multiple lines for better readability.
    Splits after every `max_words` words.
    """
    words = text.split()
    lines = []
    for i in range(0, len(words), max_words):
        lines.append(" ".join(words[i:i+max_words]))
    return "<br>".join(lines)

# ----------------- HEADER -----------------
st.markdown("<div class='main-title'>🎙️ Audio to Caption Generator</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Generate neat transcripts, highlight keywords & view with timestamps</div>", unsafe_allow_html=True)

# ----------------- FILE UPLOAD & OPTIONS -----------------
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader("📂 Upload an audio file", type=["mp3", "wav", "m4a"])

with col2:
    language = st.selectbox("🌍 Select Language", 
                            options=list(SUPPORTED_LANGUAGES.keys()),
                            format_func=lambda x: SUPPORTED_LANGUAGES[x],
                            index=list(SUPPORTED_LANGUAGES.keys()).index(DEFAULT_LANGUAGE))

keywords_input = st.text_input("🔍 Enter keywords to highlight (comma separated)", "")
keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]

# ----------------- PROCESSING -----------------
if uploaded_file is not None:
    audio_path = os.path.join("audio", uploaded_file.name)
    with open(audio_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    transcriber = Transcriber()

    with st.spinner("⏳ Transcribing... please wait"):
        result = transcriber.transcribe_audio(audio_path, language=language)

    transcript = result["text"]
    highlighted_transcript = highlight_keywords(transcript, keywords)
    formatted_transcript = format_transcript(highlighted_transcript, max_words=25)
    segments = result.get("segments", [])

    # ----------------- RESULTS DISPLAY -----------------
    st.subheader("📄 Full Transcript")
    st.markdown(f"<div class='transcript-box'>{formatted_transcript}</div>", unsafe_allow_html=True)

    with st.expander("📝 Segmented Transcript with Timestamps", expanded=False):
        for seg in segments:
            seg_text = highlight_keywords(seg["text"], keywords)
            seg_text = format_transcript(seg_text, max_words=20)
            st.markdown(
                f"<div class='transcript-box'><span class='timestamp'>[{seg['start']:.2f}s - {seg['end']:.2f}s]</span><br>{seg_text}</div>", 
                unsafe_allow_html=True
            )

    # ----------------- DOWNLOAD OPTIONS -----------------
    st.markdown("### ⬇️ Download Options")
    colA, colB = st.columns(2)

    with colA:
        st.download_button("📥 Download Full Transcript",
                           transcript,
                           file_name="transcript.txt")

    with colB:
        seg_text_all = "\n".join([f"[{s['start']:.2f} - {s['end']:.2f}] {s['text']}" for s in segments])
        st.download_button("📥 Download Segmented Transcript",
                           seg_text_all,
                           file_name="segments.txt")
