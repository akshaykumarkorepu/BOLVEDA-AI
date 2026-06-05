from src.utils import load_vectorstore

vector_store = load_vectorstore()


def retrieve_chunks(query, k=3):
    # Prevent empty queries
    if query is None or query.strip() == "":
        return []

    results = vector_store.similarity_search(query, k=k)

    return results
