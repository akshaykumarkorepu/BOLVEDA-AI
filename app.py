from dotenv import load_dotenv
from src.retrieval import retrieve_chunks
from src.llm import generate_response

from memory import add_to_history, format_history

# Load .env variables
load_dotenv()

print("Vector database loaded successfully")

# CHAT LOOP STARTS HERE
while True:
    # Ask user question
    query = input("\nAsk your question: ")

    # Exit chatbot
    if query.lower() == "exit":
        print("Exiting chatbot...")
        break

    # Save user message into memory
    add_to_history("user", query)

    # Retrieve relevant chunks
    results = retrieve_chunks(query)

    # Combine retrieved chunks into one context string
    context = "\n\n".join([result.page_content for result in results])

    # Get formatted conversation history
    history = format_history()

    # Create prompt
    prompt = f"""
You are a helpful AI assistant.

Use ONLY the provided context.

If the answer is not found in the context,
say:
"I could not find this information in the provided documents."

Do not make up information.
Do not use outside knowledge.

Conversation History:
{history}

Context:
{context}

Current Question:
{query}

Answer:
"""

    print("\nRetrieved Context:\n")
    print(context)

    print("\n" + "=" * 50 + "\n")

    # Generate response
    answer = generate_response(prompt)

    # Save assistant response into memory
    add_to_history("assistant", answer)

    print("\nAnswer:\n")
    print(answer)
