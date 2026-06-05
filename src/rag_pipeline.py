from dotenv import load_dotenv
from src.retrieval import retrieve_chunks
from src.llm import stream_response
from src.memory import add_to_history, format_history

load_dotenv()

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


# SHARED RAG FUNCTION
def process_query(query):
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

    # Store full streamed response
    full_answer = ""

    # Stream chunks from LLM
    for chunk in stream_response(prompt):
        # Keep building final answer
        full_answer += chunk

        # Send chunk to UI
        yield chunk, None

    # Save assistant response into memory
    add_to_history("assistant", full_answer)

    # Send citations AFTER streaming finishes
    yield None, formatted_sources
