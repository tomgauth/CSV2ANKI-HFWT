
import os
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Initialize Eleven Labs client with API key
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# Function to sanitize file names (remove special characters)
def sanitize_filename(text):
    # Replace spaces with underscores and remove special characters
    return re.sub(r'[^a-zA-Z0-9_]+', '', text.replace(" ", "_"))

def generate_audio(text: str, voice_id="ohItIVrXTBI80RrUECOD") -> str:
    """
    Convert the input text to speech and save it as an MP3 file using Eleven Labs.
    
    Args:
    - text: The text to convert to speech.
    - voice_id: The voice ID to use for text-to-speech conversion.
    
    Returns:
    - The path to the saved MP3 file.
    """
    # Call the Eleven Labs API for text-to-speech conversion
    response = client.text_to_speech.convert(
        voice_id=voice_id,
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2",  # Use the multilingual model for conversion
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )

    # Generate a sanitized file name for the output MP3 file
    sanitized_text = sanitize_filename(text)
    save_file_path = f"{sanitized_text}.mp3"

    # Write the audio to the file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")
    
    # Return the path of the saved audio file
    return save_file_path


def generate_audio_for_prompts(file_path: str):
    """
    Read a list of prompts from a text file and generate audio for each prompt.
    
    Args:
    - file_path: Path to the text file containing the list of prompts.
    """
    try:
        # Open the file and read all lines (one prompt per line)
        with open(file_path, 'r', encoding='utf-8') as file:
            prompts = [line.strip() for line in file.readlines()]

        # Generate audio for each prompt
        for prompt in prompts:
            if prompt:
                generate_audio(prompt)

    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    # Replace 'prompts.txt' with the path to your actual prompts text file
    prompt_file_path = 'prompts.txt'
    
    generate_audio_for_prompts(prompt_file_path)