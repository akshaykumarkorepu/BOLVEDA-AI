from src.utils.utils import load_vectorstore


def retrieve_chunks(query, k=10):
    # Prevent empty queries
    if query is None or query.strip() == "":
        return []

    vector_store = load_vectorstore()

    results = vector_store.max_marginal_relevance_search(query, k=k, fetch_k=20)

    return results
