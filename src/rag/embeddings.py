import streamlit as st

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_DB_PATH = "chroma_db"


@st.cache_resource
def get_embedding_model():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


# Create vector databases from chunks
def create_vector_store(chunks):
    embedding_model = get_embedding_model()

    # Prevent empty vector creation
    if not chunks:
        return None

    # Create and store embeddings
    try:
        # Create and store embeddings
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_model,
            persist_directory=CHROMA_DB_PATH,
        )

        return vector_store

    except Exception:
        return None
