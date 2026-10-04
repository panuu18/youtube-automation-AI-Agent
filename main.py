import os
import sys

# Fix Windows console emoji printing issue
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from modules.audio_gen import create_voiceover
from modules.video_gen import render_video
from modules.youtube_upload import upload_to_youtube
from modules.researcher import generate_script

def run_youtube_automation(topic: str):
    print(f"🚀 Starting YouTube Automation Pipeline for: '{topic}'")
    
    # --- STEP 1: Research ---
    print("🧠 Step 1: Researching & writing script...")
    script_text = generate_script(topic)
    
    # --- STEP 2: Audio Generation ---
    print("🎙️ Step 2: Generating voiceover...")
    audio_path = os.path.join("assets", "voiceover.mp3")
    create_voiceover(script_text, output_file=audio_path)
    print(f"✅ Voiceover generated: {audio_path}")
    
    # --- STEP 3: Video Generation ---
    print("🎬 Step 3: Rendering video (this might take a few moments)...")
    video_path = os.path.join("assets", "final_video.mp4")
    render_video(audio_path, script_text, output_file=video_path)
    print(f"✅ Video generated: {video_path}")
    
    # --- STEP 4: YouTube Upload ---
    print("☁️ Step 4: Uploading to YouTube...")
    try:
        video_url = upload_to_youtube(
            video_path=video_path,
            title=f"The Truth About {topic}",
            description=script_text[:200] + "...",
            tags=["automation", topic, "tech"]
        )
        print(f"🎉 Success! Video published at: {video_url}")
    except FileNotFoundError as e:
        print(f"⚠️ SKIPPED UPLOAD: {e}")
        print("To enable uploading, download 'client_secret.json' from your Google Cloud Console and place it in the folder.")
    except Exception as e:
        print(f"❌ Upload Failed: {e}")

if __name__ == "__main__":
    target_topic = "How AI is changing YouTube forever in 2026"
    run_youtube_automation(target_topic)
