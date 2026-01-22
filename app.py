import streamlit as st
import whisper
import os
from fpdf import FPDF

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="GlobalTube Translator",
    page_icon="🌐",
    layout="centered"
)

st.title("🌐 GlobalTube Audio Translator")
st.markdown(
    "Upload any audio/video file and get an **English translation with timestamps** using AI."
)

# ---------------- Helper Functions ----------------
def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"[{minutes:02d}:{seconds:02d}]"

def generate_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(
        0,
        10,
        txt=text.encode("latin-1", "replace").decode("latin-1")
    )
    return pdf.output(dest="S").encode("latin-1")

# ---------------- Sidebar ----------------
st.sidebar.header("⚙ Settings")
model_size = st.sidebar.selectbox(
    "Select Whisper Model",
    ["base", "small", "medium"],
    index=1
)
st.sidebar.info(
    "• base = fastest\n• small = balanced\n• medium = most accurate"
)

# ---------------- File Upload ----------------
uploaded_file = st.file_uploader(
    "📤 Upload audio/video file",
    type=["mp3", "wav", "m4a", "mp4"]
)

# ---------------- Main Logic ----------------
if st.button("🌍 Translate to English"):

    if uploaded_file is None:
        st.warning("Please upload an audio or video file.")
    else:
        with st.status("Processing...", expanded=True) as status:

            # Save uploaded file
            file_path = "input_media"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.write("🧠 Loading Whisper model...")
            model = whisper.load_model(model_size)

            st.write("✨ Transcribing & translating...")
            result = model.transcribe(file_path, task="translate")

            status.update(
                label="Translation Complete!",
                state="complete",
                expanded=False
            )

        # ---------------- Output ----------------
        st.subheader("📜 English Translation with Timestamps")

        full_text = ""
        for segment in result["segments"]:
            line = f"{format_time(segment['start'])} {segment['text'].strip()}"
            st.write(line)
            full_text += line + "\n"

        # ---------------- PDF Download ----------------
        pdf_data = generate_pdf(full_text)
        st.download_button(
            label="📥 Download as PDF",
            data=pdf_data,
            file_name="translation.pdf",
            mime="application/pdf"
        )

        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)

# ---------------- Footer ----------------
st.sidebar.markdown("---")
st.sidebar.write("Developed by **Meenakshi Prasanth** | CSE Project 2026")
