# YouTube Automator - Project Status

## 🚀 Progress so far:
- **Project Scaffolded:** Created the main Python project structure.
- **Audio Generator (`audio_gen.py`):** Completed using `edge-tts`.
- **Video Generator (`video_gen.py`):** Completed using `moviepy` and `Pillow`.
- **YouTube Uploader (`youtube_upload.py`):** Code written, waiting for API credentials.
- **Main Orchestrator (`main.py`):** Linked everything together.

## 🛑 Where we left off:
We stopped right before setting up the Google Cloud API. The user needs to follow the instructions to generate the YouTube Data API v3 credentials.

## ⏭️ Next Steps for Next Time:
1. User drops the downloaded `client_secret.json` into this folder.
2. Run `python main.py` to test the automatic upload to YouTube (it will trigger a one-time browser login).
3. Connect a real AI (like Gemini or OpenAI API) inside `researcher.py` so it writes real trending scripts instead of the hardcoded test script.
