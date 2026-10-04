import os
import json
import re
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
import yt_dlp
from moviepy import VideoFileClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw
from dotenv import load_dotenv

load_dotenv()

def create_credit_overlay(text: str, output_path: str):
    """Creates a transparent image with the credit text for the video overlay."""
    img = Image.new('RGBA', (720, 1280), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    
    # Draw a semi-transparent black background box at the bottom
    box_x0, box_y0 = 60, 1100
    box_x1, box_y1 = 660, 1150
    d.rectangle([box_x0, box_y0, box_x1, box_y1], fill=(0, 0, 0, 180))
    
    # Draw the text
    d.text((box_x0 + 20, box_y0 + 15), text, fill=(255, 255, 255))
    
    img.save(output_path)
    return output_path

def get_transcript(video_id: str):
    print("📜 Fetching transcript...")
    try:
        # Techno Gamerz speaks Hindi, so we try Hindi first, then English
        api = YouTubeTranscriptApi()
        transcript_list = api.fetch(video_id, languages=['hi', 'en', 'en-IN'])
        
        # Format transcript with timestamps so AI knows exactly when things happen
        formatted_transcript = ""
        for item in transcript_list:
            start = int(item['start'])
            text = item['text'].replace('\n', ' ')
            formatted_transcript += f"[{start}s] {text}\n"
            
        return formatted_transcript
    except Exception as e:
        print(f"❌ Could not get transcript: {e}")
        return None

def analyze_transcript(transcript_text: str, channel_name: str):
    print("🤖 Asking Gemini AI to find the most viral 60-second moment...")
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    # Limit transcript to first 30,000 characters to keep it fast
    transcript_text = transcript_text[:30000] 
    
    prompt = f"""
    You are an expert YouTube Shorts editor. Read the following transcript from a {channel_name} gaming video.
    Find the most intense, funny, or viral 60-second segment (between 45 to 60 seconds long).
    
    Transcript:
    {transcript_text}
    
    Output ONLY valid JSON in this exact format:
    {{
        "start_time": 120,
        "end_time": 180,
        "title": "Viral YouTube Short Title",
        "description": "Viral description here with hashtags. Watch full video on {channel_name}!"
    }}
    """
    
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )
    
    # Clean the JSON output
    json_text = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(json_text)

def download_video(video_id: str, output_path: str):
    print(f"📥 Downloading full video {video_id}...")
    if os.path.exists(output_path):
        print("✅ Video already downloaded!")
        return output_path
        
    ydl_opts = {
        'format': 'b', # Best single file (mp4) to avoid ffmpeg merging issues
        'outtmpl': output_path,
        'quiet': True,
        'noplaylist': True,
    }
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    return output_path

def edit_viral_clip(video_path: str, start_time: int, end_time: int, channel_name: str, output_path: str):
    print("✂️ Cutting and cropping video into a Short...")
    video_clip = VideoFileClip(video_path)
    
    # 1. Cut the viral moment
    short_clip = video_clip.subclipped(start_time, end_time)
    
    # 2. Crop to 9:16 (Vertical)
    w, h = short_clip.size
    target_w = int(h * (9/16))
    x_center = w / 2
    short_clip = short_clip.cropped(
        x1=x_center - target_w/2, 
        y1=0, 
        x2=x_center + target_w/2, 
        y2=h
    ).resized(new_size=(720, 1280))
    
    # 3. Add Credit Overlay
    assets_dir = os.path.dirname(output_path)
    os.makedirs(assets_dir, exist_ok=True)
    overlay_path = os.path.join(assets_dir, "credit_overlay.png")
    
    credit_text = f"Full video on: {channel_name}"
    create_credit_overlay(credit_text, overlay_path)
    
    text_clip = ImageClip(overlay_path).with_duration(short_clip.duration)
    
    # Combine
    final_video = CompositeVideoClip([short_clip, text_clip])
    
    print("🎬 Rendering final Short (this might take a minute)...")
    final_video.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac", logger=None)
    
    # Cleanup memory
    video_clip.close()
    short_clip.close()
    text_clip.close()
    final_video.close()
    
    print(f"✅ Final Viral Short saved to {output_path}")

def generate_viral_clip(video_id: str, channel_name: str):
    print(f"\n🚀 Starting Viral Clipper Bot for {channel_name} (Video ID: {video_id})")
    
    # 1. Get Transcript
    transcript = get_transcript(video_id)
    if not transcript:
        return
        
    # 2. Ask Gemini for the best moment
    data = analyze_transcript(transcript, channel_name)
    print(f"✨ AI Found Viral Moment! {data['start_time']}s to {data['end_time']}s")
    print(f"📝 Title: {data['title']}")
    
    # 3. Download the video
    assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))
    os.makedirs(assets_dir, exist_ok=True)
    full_video_path = os.path.join(assets_dir, f"full_{video_id}.mp4")
    
    download_video(video_id, full_video_path)
    
    # 4. Edit it
    final_short_path = os.path.join(assets_dir, f"viral_short_{video_id}.mp4")
    edit_viral_clip(full_video_path, data['start_time'], data['end_time'], channel_name, final_short_path)
    
    return {
        "video_path": final_short_path,
        "title": data['title'],
        "description": data['description']
    }

if __name__ == "__main__":
    # Test on a very popular Techno Gamerz GTA V video (ID: Lz210wVf45E)
    test_video_id = "Lz210wVf45E"
    generate_viral_clip(test_video_id, "Techno Gamerz")
