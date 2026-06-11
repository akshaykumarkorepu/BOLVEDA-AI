import os

from src.ingestion.pdf_loader import load_pdf
from src.ingestion.chunking import create_chunks
from src.rag.embeddings import create_vector_store


def ingest_pdf(pdf_path, original_filename=None):
    # Validate PDF path
    if not pdf_path or not os.path.exists(pdf_path):
        raise FileNotFoundError("PDF file not found.")

    try:
        # Step 1: Load PDF
        documents = load_pdf(pdf_path)

        print("PDF loaded successfully")

    except Exception:
        raise Exception("Failed to load PDF.")

    # Prevent empty document ingestion
    if not documents:
        raise Exception("No readable content found in PDF.")

    # Step 2: Create chunks
    chunks = create_chunks(documents)

    print("Chunks created successfully")

    # Prevent empty chunk creation
    if not chunks:
        raise Exception("Failed to create document chunks.")

    # Count total chunks created
    chunk_count = len(chunks)

    # Clean source names
    for chunk in chunks:
        if original_filename:
            chunk.metadata["source"] = original_filename

        else:
            source = chunk.metadata.get("source", "")
            chunk.metadata["source"] = os.path.basename(source)

    # Step 3: Create vector database
    vector_store = create_vector_store(chunks)

    if vector_store is None:
        raise Exception("Failed to create vector database.")

    print("Vector database created successfully")

    return chunk_count
