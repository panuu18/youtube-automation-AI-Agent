import asyncio
import edge_tts
import os

async def _create_voiceover_async(text: str, output_file: str, voice: str = "en-US-ChristopherNeural"):
    """
    Internal async function to generate speech using Microsoft Edge TTS.
    Default voice is Christopher (Male, American). 
    Other good ones: 'en-US-JennyNeural' (Female), 'en-GB-RyanNeural' (Male, British).
    """
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

def create_voiceover(text: str, output_file: str) -> str:
    """
    Generates a high-quality AI voiceover from text and saves it to an mp3 file.
    """
    # Ensure the assets directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Run the async Edge TTS generator synchronously
    asyncio.run(_create_voiceover_async(text, output_file))
    
    return output_file

if __name__ == "__main__":
    # Test the audio generator directly
    test_text = "Welcome to our automated YouTube channel. This voice was generated completely by code!"
    output_path = "../assets/test_voiceover.mp3"
    print("🎙️ Generating test voiceover...")
    create_voiceover(test_text, output_path)
    print(f"✅ Voiceover saved to {output_path}")
