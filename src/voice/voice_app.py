from recorder import record_audio
from whisper_stt import transcribe_audio

print("\nBOLVEDA Voice Assistant Started\n")

# Step 1: Record audio
record_audio()

# Step 2: Transcribe audio
transcript = transcribe_audio()

# Step 3: Print transcript
print("\nUser said:")
print(transcript)
