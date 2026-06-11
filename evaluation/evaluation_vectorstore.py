from langchain_community.vectorstores import Chroma

from src.rag.embeddings import get_embedding_model

EVALUATION_DB_PATH = "evaluation/evaluation_chroma_db"


def load_evaluation_vectorstore():
    embedding_model = get_embedding_model()

    return Chroma(
        persist_directory=EVALUATION_DB_PATH,
        embedding_function=embedding_model,
    )
