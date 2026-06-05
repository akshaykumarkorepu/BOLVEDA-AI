import whisper

# Load Whisper model
model = whisper.load_model("base")


def transcribe_audio(audio_path):
    # Transcribe audio
    result = model.transcribe(audio_path)

    return result["text"]
