from dotenv import load_dotenv
from src.retrieval import retrieve_chunks
from src.llm import generate_response

# Load .env variables
load_dotenv()

print("Vector database loaded successfully")

# Ask user question
query = input("Ask your question: ")

# Retrieve relevant chunks
results = retrieve_chunks(query)

# Combine retrieved chunks into a single context string
context = "\n\n".join([result.page_content for result in results])

# Create prompt with context and user question
prompt = f"""
You are a helpful AI assistant.

Answer the question ONLY using the provided context below.

If the answer is not present in the context,
say:
"I could not find the answer in the provided context."

Do not make up information.
Do not use outside knowledge.

Context:
{context}

Question:
{query}

Answer:
"""

print("\nRetrieved Context:\n")

print(context)

print("\n" + "=" * 50 + "\n")

# Send prompt to LLM and generate response
answer = generate_response(prompt)

print("\nAnswer:\n")

print(answer)
