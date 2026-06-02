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

    # Store citations
    sources = []

    # Loop through all retrieved chunks
    for result in results:
        source = result.metadata.get("source")
        page = result.metadata.get("page_label")

        # Create formatted citation
        sources.append(f"{source} - Page {page}")

    # Remove duplicate citations
    unique_sources = list(set(sources))

    # Format citations nicely
    formatted_sources = "\n".join([f"- {source}" for source in unique_sources])

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

    # Generate response
    answer = generate_response(prompt)

    # Save assistant response into memory
    add_to_history("assistant", answer)

    print("\nAnswer:\n")
    print(answer)

    # Display citations
    print("\nSources:\n")
    print(formatted_sources)
