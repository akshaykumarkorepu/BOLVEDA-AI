import streamlit as st

from src.rag_pipeline import process_query
from src.ingest import ingest_pdf
from src.voice.whisper_stt import transcribe_audio

# Page setup
st.set_page_config(page_title="BOLVEDA", page_icon="🤖", layout="wide")

# Sidebar
with st.sidebar:
    st.title("BOLVEDA")

    st.markdown("---")

    st.subheader("Upload PDF")

    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file:
        # Save uploaded PDF
        save_path = f"data/uploads/{uploaded_file.name}"

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Generate embeddings
        with st.spinner("Processing PDF..."):
            ingest_pdf(save_path)

        st.success("PDF processed successfully!")

    st.markdown("---")

    if st.button("Clear Chat"):
        st.session_state.messages = []

# Session memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main UI
st.title("BOLVEDA AI Assistant")

st.caption("Multimodal RAG-powered document assistant")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Bottom input section
col1, col2 = st.columns([8, 1])

with col1:
    user_input = st.chat_input("Ask a question...")

with col2:
    audio_value = st.audio_input("")


# Handle voice input
if audio_value:
    # Save audio temporarily
    audio_path = "temp/input.wav"

    with open(audio_path, "wb") as f:
        f.write(audio_value.read())

    # Convert speech to text
    with st.spinner("Transcribing audio..."):
        transcript = transcribe_audio(audio_path)

    # Show transcript
    st.info(f"You said: {transcript}")

    # Use transcript as query
    user_input = transcript

# Handle chat interaction
if user_input:
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate real AI response
    with st.spinner("Thinking..."):
        answer, sources = process_query(user_input)

        assistant_response = f"""
{answer}

### Sources:
{sources}
"""

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_response}
    )

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
