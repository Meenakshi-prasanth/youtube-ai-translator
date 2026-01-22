import streamlit as st
import yt_dlp
import whisper
import os
from fpdf import FPDF

# --- UI Setup ---
st.set_page_config(page_title="GlobalTube Translator", page_icon="🌐")
st.title("🌐 YouTube Audio Translator")
st.markdown("Translate any YouTube video directly into English, even without captions.")

# --- Helper Functions ---
def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"[{minutes:02d}:{seconds:02d}]"

def generate_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=text.encode("latin-1", "replace").decode("latin-1"))
    return pdf.output(dest="S").encode("latin-1")

def download_audio(url):
    st.write("🎧 Downloading audio from YouTube...")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "temp_audio.%(ext)s",
        "quiet": True,
        "noplaylist": True,
        "user_agent": "Mozilla/5.0",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        st.error(f"❌ YouTube download failed:\n\n{e}")
        return False

# --- Sidebar ---
st.sidebar.header("Settings")
model_size = st.sidebar.selectbox(
    "Select AI Model:", ["base", "small", "medium"], index=1
)
st.sidebar.info("Tip: 'base' is fastest, 'medium' is most accurate.")

# --- Main App ---
url = st.text_input("Paste YouTube URL here:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Translate Video"):
    if not url:
        st.warning("Please enter a valid YouTube URL.")
    else:
        try:
            with st.status("Processing...", expanded=True):
                # 1. Download audio
                if not download_audio(url):
                    st.stop()

                # 2. Load Whisper
                st.write(f"🧠 Loading Whisper AI ({model_size} model)...")
                model = whisper.load_model(model_size)

                # 3. Transcribe & translate
                st.write("✨ Transcribing and translating to English...")
                result = model.transcribe("temp_audio.mp3", task="translate")

            st.success("Translation Complete!")

            # --- Results ---
            st.subheader("English Translation with Timestamps")
            full_transcript = ""

            for segment in result["segments"]:
                entry = f"{format_time(segment['start'])} {segment['text'].strip()}"
                st.write(entry)
                full_transcript += entry + "\n"

            # --- PDF Download ---
            pdf_bytes = generate_pdf(full_transcript)
            st.download_button(
                "📥 Download Translation as PDF",
                data=pdf_bytes,
                file_name="translated_video.pdf",
                mime="application/pdf",
            )

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.info("Make sure FFmpeg is installed.")

        finally:
            # Cleanup
            for f in ["temp_audio.mp3", "temp_audio.webm"]:
                if os.path.exists(f):
                    os.remove(f)

st.sidebar.markdown("---")
st.sidebar.write("Developed by Meenakshi Prasanth | CSE Project 2026")









