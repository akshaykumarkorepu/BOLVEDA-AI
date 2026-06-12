import streamlit as st
import tempfile
import shutil
import os

from langchain_community.vectorstores import Chroma
from src.rag.embeddings import get_embedding_model

# Absolute ChromaDB path
CHROMA_DB_PATH = os.path.join(tempfile.gettempdir(), "chroma_db")


@st.cache_resource
def load_vectorstore():
    os.makedirs(CHROMA_DB_PATH, exist_ok=True)
    embedding_model = get_embedding_model()

    vector_store = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embedding_model,
    )

    return vector_store


def clear_vectorstore():
    # Clear Streamlit cache first
    load_vectorstore.clear()

    if os.path.exists(CHROMA_DB_PATH):
        try:
            shutil.rmtree(CHROMA_DB_PATH)

        except Exception:
            pass

    os.makedirs(CHROMA_DB_PATH, exist_ok=True)
