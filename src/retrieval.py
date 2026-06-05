from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Local embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = Chroma(persist_directory="chroma_db", embedding_function=embedding_model)


def retrieve_chunks(query, k=3):
    results = vector_store.similarity_search(query, k=k)

    return results
