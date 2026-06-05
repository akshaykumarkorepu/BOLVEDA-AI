from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Local embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ChromaDB storage path
CHROMA_DB_PATH = "chroma_db"


# Create vector databases from chunks
def create_vector_store(chunks):
    # Create and store embeddings
    vector_store = Chroma.from_documents(
        documents=chunks,  # chunked documents
        embedding=embedding_model,  # embedding generator
        persist_directory=CHROMA_DB_PATH,
    )

    return vector_store
