from dotenv import load_dotenv
from src.retrieval import retrieve_chunks

# Load .env variables
load_dotenv()

print("Vector database loaded successfully")

# Ask user question
query = input("Ask your question: ")

# Retrieve relevant chunks
results = retrieve_chunks(query)

print("\nRetrieved Chunks:\n")

for i, result in enumerate(results, start=1):
    print(f"Chunk {i}:\n")

    print(result.page_content)

    print("\n" + "-" * 50 + "\n")
