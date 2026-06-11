from langchain_community.vectorstores import Chroma

from src.ingestion.pdf_loader import load_pdf
from src.ingestion.chunking import create_chunks
from src.rag.embeddings import get_embedding_model

EVALUATION_DB_PATH = "evaluation/evaluation_chroma_db"


def build_evaluation_db(pdf_path):
    # Load PDF
    documents = load_pdf(pdf_path)

    # Create chunks
    chunks = create_chunks(documents)

    # Embedding model
    embedding_model = get_embedding_model()

    # Build evaluation-only Chroma DB
    Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=EVALUATION_DB_PATH,
    )

    print("Evaluation vector database created successfully.")
