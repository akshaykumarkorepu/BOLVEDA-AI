from dotenv import load_dotenv
import os
import shutil

from src.pdf_loader import load_pdf
from src.chunking import create_chunks
from src.embeddings import create_vector_store

# Load .env variables
load_dotenv()

# ChromaDB storage path
CHROMA_DB_PATH = "chroma_db"


def ingest_pdf(pdf_path):
    # Clear old vector database
    if os.path.exists(CHROMA_DB_PATH):
        shutil.rmtree(CHROMA_DB_PATH)

    # Step 1: Load PDF
    documents = load_pdf(pdf_path)

    print("PDF loaded successfully")

    # Step 2: Create chunks
    chunks = create_chunks(documents)

    print("Chunks created successfully")

    # Clean source names
    for chunk in chunks:
        source = chunk.metadata.get("source", "")
        chunk.metadata["source"] = os.path.basename(source)

    # Step 3: Create vector database
    create_vector_store(chunks)

    print("Vector database created successfully")
