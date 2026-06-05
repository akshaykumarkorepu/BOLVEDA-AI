import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("ELEVENLABS_API_KEY")

# Create ElevenLabs client
client = ElevenLabs(api_key=api_key)


def generate_speech(text, output_path="temp/output.mp3"):
    # Generate audio stream
    audio = client.text_to_speech.convert(
        voice_id="JBFqnCBsd6RMkjVDRZzb", model_id="eleven_multilingual_v2", text=text
    )

    # Save audio to file
    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    return output_path
