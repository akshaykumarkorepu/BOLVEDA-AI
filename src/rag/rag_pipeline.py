from src.rag.retrieval import retrieve_chunks
from src.rag.llm import stream_response
from src.memory.memory import add_to_history, format_history

# SYSTEM PROMPT
SYSTEM_PROMPT = """
You are BOLVEDA, a professional AI assistant that answers questions strictly using the provided document context.

Behavior Rules:
1. Answer ONLY using the provided context.
2. Never invent, assume, or hallucinate information.
3. If the answer is not present in the context, clearly say:
   "I could not find that information in the provided documents."
4. Keep responses concise, conversational, and natural.
5. Avoid robotic formatting and unnecessary repetition.
6. Prefer short paragraphs or brief bullet points when helpful.
7. Keep responses under 100 words unless the user explicitly asks for more detail.
8. Focus only on the most relevant information.
9. Avoid overly technical wording unless the user asks for it.
10. Do not use outside knowledge.
11. Stay grounded in the retrieved context at all times.

Response Style:
- Sound like a helpful conversational AI assistant.
- Be clear, direct, and confident.
- Use smooth conversational phrasing.
- Avoid overly formal language.
- Avoid long explanations unless requested.

Important:
- Never mention information outside the retrieved documents.
- Do not fabricate missing details.
- If context is insufficient, say so clearly.
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

Answer the user's question naturally and conversationally using ONLY the provided context.
Keep the response concise, clear, and conversational.
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
