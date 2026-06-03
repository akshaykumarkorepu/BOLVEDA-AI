from dotenv import load_dotenv
from src.retrieval import retrieve_chunks
from src.llm import generate_response

from memory import add_to_history, format_history

# Load .env variables
load_dotenv()

print("Vector database loaded successfully")

# SYSTEM PROMPT
SYSTEM_PROMPT = """
You are a professional AI assistant answering questions strictly from provided documents.

Rules:
1. Answer ONLY using the provided context.
2. Do NOT make up information.
3. If the answer is not present in the context, say:
   "I could not find that information in the provided documents."
4. Be concise and accurate.
5. Never assume facts not explicitly stated.
6. Do not use outside knowledge.
7. If context is insufficient, clearly state that.

Output Format:

Summary:
- Give a short 1-2 sentence summary.

Detailed Answer:
- Provide a slightly more detailed explanation using ONLY the retrieved context.

Do NOT mention anything outside the provided context.
"""

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

{SYSTEM_PROMPT}

Conversation History:
{history}

Context:
{context}

Current Question:
{query}

Generate the response in the following format:

Summary:
- Short concise answer

Detailed Answer:
- More detailed explanation using ONLY the retrieved context
"""

    # Generate response
    answer = generate_response(prompt)

    # Save assistant response into memory
    add_to_history("assistant", answer)

    print("\nAnswer:\n")
    print(answer)

    # Print citations ONLY if answer was found
    if "I could not find" not in answer:
        print("\nSources:\n")
        print(formatted_sources)
