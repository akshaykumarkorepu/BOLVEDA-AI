from evaluation.evaluation_vectorstore import (
    load_evaluation_vectorstore,
)


def retrieve_evaluation_chunks(query, k=10):
    if query is None or query.strip() == "":
        return []

    if k <= 0:
        return []

    try:
        vector_store = load_evaluation_vectorstore()

        results = vector_store.max_marginal_relevance_search(
            query,
            k=k,
            fetch_k=20,
        )

        if not results:
            return []

        return results

    except Exception:
        return []
