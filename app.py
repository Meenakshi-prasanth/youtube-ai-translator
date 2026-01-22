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
    """Converts seconds to [MM:SS] format"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"[{minutes:02d}:{seconds:02d}]"

def generate_pdf(text):
    """Creates a PDF from the translation text"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Using encode('latin-1', 'replace') to avoid special character errors
    pdf.multi_cell(0, 10, txt=text.encode('latin-1', 'replace').decode('latin-1'))
    return pdf.output(dest='S').encode('latin-1')

# --- Sidebar / Settings ---
st.sidebar.header("Settings")
model_size = st.sidebar.selectbox("Select AI Model:", ["base", "small", "medium"], index=1)
st.sidebar.info("Tip: 'base' is fastest, 'medium' is most accurate.")

# --- Main App Logic ---
url = st.text_input("Paste YouTube URL here:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Translate Video"):
    if url:
        try:
            with st.status("Processing...", expanded=True) as status:
                # 1. Download Audio
                st.write("📥 Downloading audio from YouTube...")
               # 1. Download Audio
                st.write("📥 Downloading audio from YouTube...")
                
                # This tells Python to look in your project folder for the .exe files
                ydl_opts = {
                  'format': 'bestaudio/best',
                  'outtmpl': 'temp_audio.%(ext)s',
                  'ffmpeg_location': '/usr/bin/ffmpeg',
                  'quiet': True,
                  'no_warnings': True,
                  'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                  'postprocessors': [{
                      'key': 'FFmpegExtractAudio',
                      'preferredcodec': 'mp3',
                      'preferredquality': '192',
                  }],
               }
 
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                # 2. Load Whisper Model
                st.write(f"🧠 Loading Whisper AI ({model_size} model)...")
                model = whisper.load_model(model_size)
                
                # 3. Transcribe & Translate
                st.write("✨ Transcribing and translating to English...")
                result = model.transcribe("temp_audio.mp3", task="translate")
                
                status.update(label="Translation Complete!", state="complete", expanded=False)

            # --- Display Results ---
            st.subheader("English Translation with Timestamps:")
            full_transcript = ""

            for segment in result['segments']:
                timestamp = format_time(segment['start'])
                text = segment['text'].strip()
                entry = f"{timestamp} {text}"
                st.write(entry) # Display line by line
                full_transcript += entry + "\n"

            # --- Download Button ---
            pdf_bytes = generate_pdf(full_transcript)
            st.download_button(
                label="📥 Download Translation as PDF",
                data=pdf_bytes,
                file_name="translated_video.pdf",
                mime="application/pdf"
            )
            
            # Cleanup temporary file
            if os.path.exists("temp_audio.mp3"):
                os.remove("temp_audio.mp3")

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.info("Note: Make sure you have FFmpeg installed on your system.")
    else:
        st.warning("Please enter a valid URL.")
# Cleanup all temporary files after the download button
    # Cleanup all temporary files after the download button
    for temp_file in ["temp_audio.mp3", "temp_audio.webm"]:
        if os.path.exists(temp_file):
            os.remove(temp_file)
            st.sidebar.markdown("---")

st.sidebar.write("Developed by [Meenakshi Prasanth] | CSE Project 2026")





