import streamlit as st
from src.rag_pipeline import process_query

# Page setup
st.set_page_config(page_title="BOLVEDA", page_icon="🤖", layout="wide")

# Sidebar
with st.sidebar:
    st.title("BOLVEDA")

    st.markdown("---")

    st.subheader("Upload PDF")

    st.info("PDF upload feature coming soon")

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

# User input
user_input = st.chat_input("Ask a question...")

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
