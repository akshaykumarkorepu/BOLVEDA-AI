import time
import os
import tempfile
import streamlit as st

from src.rag.rag_pipeline import process_query
from src.ingestion.ingest import ingest_pdf
from src.memory.memory import clear_history
from src.utils.utils import clear_vectorstore

# Page setup
st.set_page_config(page_title="BOLVEDA", page_icon="🤖", layout="wide")

# Initialize session memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Track processed PDFs
if "processed_files" not in st.session_state:
    st.session_state.processed_files = set()

# Reset file uploader when ending session
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

# Sidebar
with st.sidebar:
    st.title("🧠 Your AI Workspace")

    st.caption("⚠️ Do not upload confidential or sensitive documents.")

    st.markdown("---")

    st.subheader("Upload PDF")

    uploaded_file = st.file_uploader(
        "Upload a PDF",
        type="pdf",
        key=f"uploader_{st.session_state.uploader_key}",
    )

    # Validate uploaded file
    if uploaded_file:
        # Allow only real PDFs
        if uploaded_file.type != "application/pdf":
            st.error("❌ Only PDF files are allowed.")
            st.stop()

        # File size limit (200MB)
        MAX_FILE_SIZE = 200 * 1024 * 1024

        if uploaded_file.size > MAX_FILE_SIZE:
            st.error("❌ PDF too large. Maximum size is 200MB.")
            st.stop()

        # Process ONLY if not already processed
        if uploaded_file.name not in st.session_state.processed_files:
            with st.spinner("Processing PDF..."):
                temp_path = None

                try:
                    # Create temporary PDF file
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=".pdf"
                    ) as temp_file:
                        temp_file.write(uploaded_file.getbuffer())

                        temp_path = temp_file.name

                    # Clear previous vector database
                    clear_vectorstore()

                    # Process PDF and generate embeddings
                    ingest_pdf(temp_path, uploaded_file.name)

                    st.success("✅ PDF processed successfully!")

                    # Mark as processed
                    st.session_state.processed_files.add(uploaded_file.name)

                except Exception:
                    st.error("❌ Failed to process PDF. Please upload a valid PDF.")
                    st.stop()

                    st.stop()

                finally:
                    # Always delete temporary file
                    if temp_path and os.path.exists(temp_path):
                        os.remove(temp_path)

        # Active document display
        st.write(f"📄 Active Document: {uploaded_file.name}")

    st.markdown("---")

    # Recent session chats
    st.subheader("🕘 Current Session")

    if len(st.session_state.messages) == 0:
        st.caption("No active chats yet.")

    else:
        # Show recent user questions only
        recent_questions = [
            msg["content"] for msg in st.session_state.messages if msg["role"] == "user"
        ]

        # Display last 5 questions
        for question in recent_questions[-5:]:
            st.caption(f"🗨️ {question[:50]}...")

    st.markdown("---")

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []

        clear_history()

        st.rerun()

    # End document session
    if st.button("End Document Session"):
        clear_vectorstore()

        clear_history()

        st.session_state.messages = []

        st.session_state.processed_files = set()

        # Reset file uploader
        st.session_state.uploader_key += 1

        st.success("✅ Document session ended.")

        st.rerun()

# Main UI
st.title("BOLVEDA AI")

st.markdown("#### Transform documents into intelligent conversations")

st.markdown("<br>", unsafe_allow_html=True)

# Display previous chat history
for message in st.session_state.messages:
    avatar = (
        ":material/person:" if message["role"] == "user" else ":material/smart_toy:"
    )

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask something about your document...")

# Prevent questions without PDF
if user_input and uploaded_file is None:
    st.warning("⚠️ Please upload a PDF before asking questions.")

    st.stop()

# Handle valid questions
if user_input and user_input.strip():
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

        try:
            # Stream response
            for chunk, citation in process_query(user_input):
                # Stream chunk
                if chunk:
                    full_response += chunk

                    response_placeholder.markdown(full_response + "▌")

                # Extract citations
                if citation:
                    sources = citation["sources"]

                    latency_ms = citation["latency_ms"]

        except Exception:
            thinking_placeholder.empty()

            st.error("❌ Failed to generate response.")

            st.stop()

        # Remove thinking flow
        thinking_placeholder.empty()

        # Empty response fallback
        if not full_response.strip():
            full_response = "⚠️ No relevant answer found in the document."

        # Final response without cursor
        response_placeholder.markdown(full_response)

        # Display citations
        if sources:
            with st.expander("📚 Sources & Citations"):
                st.markdown(sources)

        # Save assistant response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": full_response,
            }
        )
