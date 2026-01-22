
🌐 GlobalTube Audio Translator

An AI-powered web application that translates multilingual audio/video files into English using OpenAI’s Whisper model. The app generates timestamped translations and allows users to download the output as a PDF.

> ⚠️ Note: Direct YouTube audio extraction is restricted on cloud platforms due to YouTube’s content protection policies. Hence, this application supports user-uploaded media files for reliability and legal compliance.




---

🚀 Features

🎧 Upload audio/video files (.mp3, .wav, .m4a, .mp4)

🌍 Automatic language detection

🧠 AI-based transcription & translation using Whisper

⏱ Timestamped English translation

📄 Download translated text as a PDF

☁️ Deployed on Streamlit Cloud (shareable public link)



---

🛠 Tech Stack

Frontend & App Framework: Streamlit

AI Model: OpenAI Whisper

Audio Processing: FFmpeg

PDF Generation: FPDF

Language: Python



---

📂 Project Structure

GlobalTube-Translator/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation


---

⚙️ Installation (Run Locally)

1. Clone the repository



git clone https://github.com/your-username/GlobalTube-Translator.git
cd GlobalTube-Translator

2. Install dependencies



pip install -r requirements.txt

3. Install FFmpeg



Windows: https://ffmpeg.org/download.html

Linux:


sudo apt install ffmpeg

4. Run the app



streamlit run app.py


---

🌐 Deployment

This project is deployed using Streamlit Cloud, providing a public and shareable link.

Steps:

1. Push the repository to GitHub


2. Connect GitHub repo to Streamlit Cloud


3. Deploy 🎉




---

🧠 How It Works

1. User uploads an audio/video file


2. Whisper model automatically detects the language


3. Audio is transcribed and translated into English


4. Output is displayed with timestamps


5. User can download the translation as a PDF




---

⚠️ Why YouTube URLs Are Not Used

YouTube restricts automated media extraction on cloud platforms, often resulting in 403 Forbidden errors.
To ensure:

Reliability

Legal compliance

Consistent performance


This application uses direct media upload instead of YouTube URLs.


---

🎓 Academic Use

This project is suitable for:

Mini / Final Year Project

AI / ML coursework

NLP demonstrations

Portfolio for MS applications



---

👩‍💻 Author

Meenakshi Prasanth
B.Tech Computer Science Engineering
Class of 2025


---

📜 License

This project is intended for educational and research purposes only.


---




Just tell me 😄
