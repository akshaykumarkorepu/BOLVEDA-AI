from src.utils.utils import load_vectorstore


def retrieve_chunks(query, k=3):
    # Prevent empty queries
    if query is None or query.strip() == "":
        return []

    vector_store = load_vectorstore()

    results = vector_store.similarity_search_with_score(query, k=k)

    filtered_results = []

    for doc, score in results:
        # Lower score = better similarity
        if score < 1.5:
            filtered_results.append(doc)

    return filtered_results
