import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
import yt_dlp
from moviepy import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, ColorClip

def get_background_video(output_path: str, duration: float):
    """Returns the user-provided gameplay video, or a colorful fallback."""
    if os.path.exists(output_path):
        return VideoFileClip(output_path)
        
    print(f"\n⚠️  Note: Could not find '{output_path}'.")
    print("To use real Minecraft gameplay, please download any gameplay .mp4 and save it as 'assets/minecraft_bg.mp4'.")
    print("For now, generating a dynamic color background!\n")
    
    # Fallback to a dark blue vertical background
    return ColorClip(size=(720, 1280), color=(20, 30, 60), duration=duration)

def create_text_overlay(text: str, output_path: str):
    """Creates a transparent image with large centered text."""
    # Create a 720x1280 transparent image (YouTube Shorts format)
    img = Image.new('RGBA', (720, 1280), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    
    # Wrap the text so it fits on screen
    wrapped_text = textwrap.fill(text[:150] + "...", width=30)
    
    # Draw a semi-transparent black background box for readability
    box_x0, box_y0 = 60, 450
    box_x1, box_y1 = 660, 830
    d.rectangle([box_x0, box_y0, box_x1, box_y1], fill=(0, 0, 0, 180))
    
    # Draw the text
    # Note: Using default font since custom TTF paths vary by OS.
    # In a production app, we would load a custom font like Montserrat.ttf
    d.text((box_x0 + 40, box_y0 + 40), wrapped_text, fill=(255, 255, 255))
    
    img.save(output_path)
    return output_path

def render_video(audio_path: str, script_text: str, output_file: str) -> str:
    """Combines gameplay, audio, and text into a vertical mp4."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    assets_dir = os.path.dirname(output_file)
    
    # 1. Get the background video path
    bg_video_path = os.path.join(assets_dir, "minecraft_bg.mp4")
    
    # 2. Create the text overlay
    text_img_path = os.path.join(assets_dir, "text_overlay.png")
    create_text_overlay(script_text, text_img_path)
    
    # 3. Load audio to get duration
    audio_clip = AudioFileClip(audio_path)
    duration = audio_clip.duration
    
    # 4. Load video or fallback, crop to 9:16 (vertical), and trim to audio duration
    video_clip = get_background_video(bg_video_path, duration)
    
    if hasattr(video_clip, 'size') and video_clip.size[0] != 720:
        # Calculate crop for center 9:16 if it's a real video
        w, h = video_clip.size
        target_w = int(h * (9/16))
        x_center = w / 2
        video_clip = video_clip.cropped(
            x1=x_center - target_w/2, 
            y1=0, 
            x2=x_center + target_w/2, 
            y2=h
        ).resized(new_size=(720, 1280))
        
        # Loop or cut the video to match the audio
        from moviepy.video.fx import Loop
        if video_clip.duration < duration:
            video_clip = video_clip.with_effects([Loop(duration=duration)])
        else:
            video_clip = video_clip.subclipped(0, duration)
        
    # 5. Load the text overlay
    text_clip = ImageClip(text_img_path).with_duration(duration)
    
    # 6. Composite the video and text
    final_video = CompositeVideoClip([video_clip, text_clip])
    
    # 7. Add audio
    final_video = final_video.with_audio(audio_clip)
    
    # 8. Export
    final_video.write_videofile(
        output_file, 
        fps=30, 
        codec="libx264", 
        audio_codec="aac",
        logger=None
    )
    
    # Close clips to free memory
    audio_clip.close()
    video_clip.close()
    text_clip.close()
    final_video.close()
    
    return output_file
