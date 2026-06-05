import pyaudio
import wave

# Audio configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5
OUTPUT_FILE = "input.wav"


def record_audio():
    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open microphone stream
    stream = audio.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )

    print("Recording... Speak now.")

    frames = []

    # Record audio
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording finished.")

    # Stop stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save WAV file
    with wave.open(OUTPUT_FILE, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))

    print(f"Audio saved as {OUTPUT_FILE}")


# Run independently if executed directly
if __name__ == "__main__":
    record_audio()
