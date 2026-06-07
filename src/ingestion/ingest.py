import os

from src.ingestion.pdf_loader import load_pdf
from src.ingestion.chunking import create_chunks
from src.rag.embeddings import create_vector_store


def ingest_pdf(pdf_path):
    # Step 1: Load PDF
    documents = load_pdf(pdf_path)

    print("PDF loaded successfully")

    # Step 2: Create chunks
    chunks = create_chunks(documents)

    print("Chunks created successfully")

    # Count total chunks created
    chunk_count = len(chunks)

    # Clean source names
    for chunk in chunks:
        source = chunk.metadata.get("source", "")
        chunk.metadata["source"] = os.path.basename(source)

    # Step 3: Create vector database
    create_vector_store(chunks)

    print("Vector database created successfully")

    # Return chunk count for logging
    return chunk_count
