from src.ingestion.pdf_loader import load_pdf


docs = load_pdf("tests/test_data/sample.pdf")

print("\nPDF Loaded Successfully\n")

print(docs[1].page_content[:500])
