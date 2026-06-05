import streamlit as st

from src.rag.rag_pipeline import process_query
from src.ingestion.ingest import ingest_pdf
from src.memory.memory import clear_history


# Page setup
st.set_page_config(page_title="BOLVEDA", page_icon="🤖", layout="wide")

# Sidebar
with st.sidebar:
    st.title("BOLVEDA")

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

            # Generate embeddings
            with st.spinner("Processing PDF..."):
                ingest_pdf(save_path)

        # Mark as processed
        st.session_state.processed_files.add(uploaded_file.name)

        st.success("PDF processed successfully!")

    st.markdown("---")

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []

        clear_history()

        st.rerun()

# Session memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main UI
st.title("BOLVEDA AI Assistant")

st.caption("Conversational RAG-powered document assistant")

st.markdown("<br>", unsafe_allow_html=True)

# Display previous chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Ask something about your document...")


# Handle chat interaction
if user_input is not None and user_input.strip() != "":
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate streaming AI response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()

        full_response = ""

        sources = ""

        # Stream response
        for chunk, citation in process_query(user_input):
            # If chunk exists → stream it
            if chunk:
                full_response += chunk

                response_placeholder.markdown(full_response + "▌")

            # If citations arrive
            if citation:
                sources = citation

        # Final formatted response
        assistant_response = f"""
{full_response}

### Sources:
{sources}
"""

        response_placeholder.markdown(assistant_response)

        # Save assistant response
        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_response}
        )
