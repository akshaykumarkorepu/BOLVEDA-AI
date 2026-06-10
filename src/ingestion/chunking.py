from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(documents):
    # Prevent empty document chunking
    if not documents:
        return []

    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    try:
        # Split documents into chunks
        chunks = text_splitter.split_documents(documents)

        return chunks

    except Exception:
        return []
