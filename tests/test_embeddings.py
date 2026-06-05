from src.ingestion.pdf_loader import load_pdf
from src.ingestion.chunking import create_chunks
from src.rag.embeddings import create_vector_store


docs = load_pdf("data/sample.pdf")

chunks = create_chunks(docs)

vector_store = create_vector_store(chunks)

print("\nVector DB created successfully\n")
