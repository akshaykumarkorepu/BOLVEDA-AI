import streamlit as st

from langchain_community.vectorstores import Chroma
from src.rag.embeddings import get_embedding_model


@st.cache_resource
def load_vectorstore():
    embedding_model = get_embedding_model()

    vector_store = Chroma(
        persist_directory="chroma_db",
        embedding_function=embedding_model,
    )

    return vector_store
