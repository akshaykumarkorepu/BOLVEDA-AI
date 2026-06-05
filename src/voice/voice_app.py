from src.app import process_query

from src.voice.recorder import record_audio
from src.voice.whisper_stt import transcribe_audio

from voice.tts import speak

print("\nBOLVEDA Voice Assistant Started")

# Step 1: Record audio
record_audio()

# Step 2: Transcribe audio
transcript = transcribe_audio()

# Step 3: Print transcript
print("\nUser said:")
print(transcript)

# Step 4: Send transcript into RAG pipeline
answer, sources = process_query(transcript)

# Step 5: Print AI response
print("\nAnswer:\n")
print(answer)

# Step 6: Speak response aloud
speak(answer)

# Step 7: Print citations
if "I could not find" not in answer:
    print("\nSources:\n")
    print(sources)
