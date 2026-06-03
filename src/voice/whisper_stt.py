import whisper

# Load Whisper model
model = whisper.load_model("base")


def transcribe_audio():
    # Transcribe audio
    result = model.transcribe("input.wav")

    return result["text"]


# Run independently if executed directly
if __name__ == "__main__":
    transcript = transcribe_audio()

    print("\nTranscription:")
    print(transcript)
