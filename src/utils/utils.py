from langchain_community.vectorstores import Chroma
from src.rag.embeddings import get_embedding_model


def load_vectorstore(chroma_path):
    embedding_model = get_embedding_model()

    vector_store = Chroma(
        persist_directory=chroma_path,
        embedding_function=embedding_model,
    )

    return vector_store
