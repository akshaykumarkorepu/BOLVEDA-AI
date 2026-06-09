import time
import uuid
import streamlit as st

from src.rag.rag_pipeline import process_query
from src.ingestion.ingest import ingest_pdf
from src.memory.memory import clear_history
from src.utils.utils import clear_vectorstore

from db.db_logger import (
    log_document,
    log_query,
    get_total_queries,
    get_total_documents,
    get_avg_latency,
    get_recent_chats,
    get_chat_messages,
)

# Page setup
st.set_page_config(page_title="BOLVEDA", page_icon="🤖", layout="wide")

# Sidebar
with st.sidebar:
    st.title("🧠 Your AI Workspace")

    st.markdown("---")

    st.subheader("Upload PDF")

    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    # Track processed PDFs
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = set()

    if uploaded_file:
        # Save uploaded PDF
        save_path = f"data/uploads/{uploaded_file.name}"

        # Process ONLY if not already processed
        if uploaded_file.name not in st.session_state.processed_files:
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner("Processing PDF..."):
                clear_vectorstore()

                # Process PDF and get total chunks created
                chunk_count = ingest_pdf(save_path)

                # Log uploaded document into SQLite
                log_document(uploaded_file.name, chunk_count)

        # Mark as processed
        st.session_state.processed_files.add(uploaded_file.name)

        st.success("PDF processed successfully!")

        # Active document display
        st.write(f"📄 Active Document: {uploaded_file.name}")

    st.markdown("---")

    # Sidebar analytics section
    st.subheader("📊 AI Analytics")

    # Fetch total query count from SQLite
    total_queries = get_total_queries()

    # Fetch total uploaded documents count
    total_documents = get_total_documents()

    # Fetch average AI response latency
    avg_latency = get_avg_latency()

    # Display analytics metrics
    st.write(f"🧠 Total Queries: {total_queries}")

    st.write(f"📄 Documents Uploaded: {total_documents}")

    # Convert milliseconds to seconds
    avg_latency_sec = avg_latency / 1000

    # Display formatted latency
    st.write(f"⚡ Avg Latency: {avg_latency_sec:.2f} sec")

    # Divider line
    st.markdown("---")

    # Recent query history section
    st.subheader("🕘 Recent Chats")

    # Fetch recent query history from SQLite
    recent_chats = get_recent_chats()

    # Handle empty query history
    if len(recent_chats) == 0:
        st.caption("No recent chats yet.")

    # Display clickable history buttons
    else:
        # Display recent chat sessions
        for chat_id, title, timestamp in recent_chats:
            # Create clickable chat button
            if st.button(
                f"📌 {title}",
                key=f"chat_{chat_id}",
            ):
                # Store selected chat session
                st.session_state.selected_chat_id = chat_id

    # Divider line
    st.markdown("---")

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []

        clear_history()

        st.session_state.chat_id = str(uuid.uuid4())

        st.rerun()

# Initialize session memory
if "messages" not in st.session_state:
    # Store active chat messages
    st.session_state.messages = []


# Create unique chat session ID
if "chat_id" not in st.session_state:
    # Generate unique conversation ID
    st.session_state.chat_id = str(uuid.uuid4())

# Main UI
st.title("BOLVEDA AI")

st.markdown("#### Transform documents into intelligent conversations")

st.markdown("<br>", unsafe_allow_html=True)

# Display selected chat session
if "selected_chat_id" in st.session_state:
    # Fetch all messages from selected chat
    chat_messages = get_chat_messages(st.session_state.selected_chat_id)

    # Chat history title
    st.markdown("## 📜 Chat History Viewer")

    # Display full conversation thread
    for question, answer, timestamp in chat_messages:
        # Display user question
        with st.chat_message(
            "user",
            avatar=":material/person:",
        ):
            st.markdown(question)

        # Display AI response
        with st.chat_message(
            "assistant",
            avatar=":material/smart_toy:",
        ):
            st.markdown(answer)

            st.caption(f"🕒 {timestamp}")

    # Close history viewer button
    if st.button("❌ Close Chat Viewer"):
        # Remove selected chat session
        del st.session_state.selected_chat_id

        # Refresh app UI
        st.rerun()

    st.markdown("---")

# Display previous chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        avatar = ":material/person:"
    else:
        avatar = ":material/smart_toy:"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask something about your document...")


# Handle chat interaction
if user_input is not None and user_input.strip() != "":
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user", avatar=":material/person:"):
        st.markdown(user_input)

    # Generate streaming AI response
    with st.chat_message("assistant", avatar=":material/smart_toy:"):
        response_placeholder = st.empty()

        thinking_placeholder = st.empty()

        full_response = ""

        sources = ""

        latency_ms = 0

        # Thinking flow
        thinking_steps = [
            "🔍 Searching document...",
            "📚 Retrieving relevant chunks...",
            "🧠 Generating grounded response...",
            "✨ Finalizing answer...",
        ]

        # Display thinking animation
        for step in thinking_steps:
            thinking_placeholder.info(step)

            time.sleep(0.6)

        # Stream response
        for chunk, citation in process_query(user_input):
            # If chunk exists → stream it
            if chunk:
                full_response += chunk

                # Typing cursor effect
                response_placeholder.markdown(full_response + "▌")

            if citation:
                sources = citation["sources"]

                latency_ms = citation["latency_ms"]

        # Remove thinking flow
        thinking_placeholder.empty()

        # Final response without cursor
        response_placeholder.markdown(full_response)

        # Display citations
        if sources:
            with st.expander("📚 Sources & Citations"):
                st.markdown(sources)

        # Save assistant response
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )

        # Log query into SQLite database
        log_query(
            st.session_state.chat_id,
            user_input,
            full_response,
            latency_ms,
        )
