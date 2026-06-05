from src.rag.llm import stream_response


print("\nStreaming Response:\n")

for chunk in stream_response("Hello"):
    print(chunk, end="")
