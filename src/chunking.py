from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(documents):
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    # Split documents into chunks
    chunks = text_splitter.split_documents(documents)

    # Debug info
    print(f"\nTotal chunks created: {len(chunks)}\n")

    return chunks
