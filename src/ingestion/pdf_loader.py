import os
from langchain_community.document_loaders import PyPDFLoader


# Function to load pdf
def load_pdf(pdf_path):
    # Validate PDF path
    if not pdf_path or not os.path.exists(pdf_path):
        return []

    try:
        # Create PDF loader
        loader = PyPDFLoader(pdf_path)

        # Load PDF pages
        documents = loader.load()

    except Exception:
        return []

    # Handle empty PDF safely
    if not documents:
        return []

    return documents
