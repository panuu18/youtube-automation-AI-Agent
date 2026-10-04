import os
from dotenv import load_dotenv
from google import genai

# Load the API key from the .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def generate_script(topic: str) -> str:
    """
    Uses Google Gemini AI to write a highly engaging YouTube script.
    """
    print("🤖 AI is thinking...")
    
    if not api_key:
        print("⚠️ Warning: No Gemini API Key found. Using fallback script.")
        return f"Welcome back to the channel! Today we are looking at {topic}."

    try:
        # Using the newest google-genai SDK
        client = genai.Client(api_key=api_key)
        
        prompt = (
            f"Write a highly engaging, fast-paced 30-second YouTube shorts script about '{topic}'. "
            "IMPORTANT: ONLY output the exact words that will be spoken by the voiceover. "
            "Do NOT include brackets like [Intro] or [Music]. Do NOT include any visual directions. "
            "Just give me the raw spoken text."
        )
        
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )
        return response.text.strip()
    
    except Exception as e:
        print(f"❌ AI Error: {e}")
        return f"Today we are looking at {topic}. (AI generation failed)"
