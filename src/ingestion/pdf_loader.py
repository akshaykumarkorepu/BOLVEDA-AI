from langchain_community.document_loaders import PyPDFLoader


# Function to load pdf
def load_pdf(pdf_path):
    # Create PDF loader
    loader = PyPDFLoader(pdf_path)

    # Load PDF pages
    documents = loader.load()

    # Debug info
    print(f"\nTotal pages loaded:{len(documents)}\n")

    return documents
