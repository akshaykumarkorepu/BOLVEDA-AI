import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv("ELEVENLABS_API_KEY")

# Create ElevenLabs client
client = ElevenLabs(api_key=api_key)


def speak(text):
    # Convert text into speech audio
    audio = client._text_to_speech.convert(
        voice_id="JBFqnCBsd6RMkjVDRZzb", model_id="eleven_multilingual_v2", text=text
    )

    # Play generated audio
    play(audio)
