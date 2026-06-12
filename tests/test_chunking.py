from src.ingestion.pdf_loader import load_pdf
from src.ingestion.chunking import create_chunks


docs = load_pdf("tests/test_data/sample.pdf")

chunks = create_chunks(docs)

print(f"\nTotal Chunks: {len(chunks)}\n")

print(chunks[1].page_content[:300])
