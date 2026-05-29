from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


# Create vector databases from chunks
def create_vector_store(chunks):
    # Initialize embedding model
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

    # Create and store embeddings
    vector_store = Chroma.from_documents(
        documents=chunks,  # chunked documents
        embedding=embedding_model,  # embedding generator
        persist_directory="chroma_db",  # save chroma_db locally
    )

    return vector_store
