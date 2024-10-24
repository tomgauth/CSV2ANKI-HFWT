import os
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
load_dotenv() 

# Initialize Eleven Labs client with API key
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def generate_audio(text: str) -> str:
    """
    Convert the input text to speech and save it as an MP3 file using Eleven Labs.
    
    Args:
    - text: The text to convert to speech.
    
    Returns:
    - The path to the saved MP3 file.
    """
    # Call the Eleven Labs API for text-to-speech conversion
    response = client.text_to_speech.convert(
        voice_id="ohItIVrXTBI80RrUECOD",  # Adam pre-made voice
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2",  # Use turbo model for low latency
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # Generate a unique file name for the output MP3 file
    save_file_path = f"{uuid.uuid4()}.mp3"

    # Write the audio to the file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")
    
    # Return the path of the saved audio file
    return save_file_path