import streamlit as st
from src.utils.utils import load_vectorstore


def retrieve_chunks(query, k=10):
    # Prevent empty queries
    if query is None or query.strip() == "":
        return []

    # Prevent invalid retrieval size
    if k <= 0:
        return []

    try:
        # Load vector database
        vector_store = load_vectorstore(st.session_state.chroma_path)

        # Retrieve relevant chunks
        results = vector_store.max_marginal_relevance_search(
            query,
            k=k,
            fetch_k=20,
        )

        # Handle empty retrieval safely
        if not results:
            return []

        return results

    except Exception:
        # Graceful retrieval failure
        return []
