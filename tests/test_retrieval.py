from src.rag.retrieval import retrieve_chunks


queries = [
    "What is an LLM?",
    "How are LLMs aligned to human preferences?",
    "What is cosine similarity?",
    "Why are vector databases used?",
    "Who won FIFA 2014?",
]


for query in queries:
    print("\n" + "=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)

    results = retrieve_chunks(query)

    if not results:
        print("No chunks retrieved.")
        continue

    for i, result in enumerate(results):
        print(f"\n--- CHUNK {i + 1} ---\n")

        print(result.page_content[:700])

        print("\nMETADATA:")
        print(result.metadata)

        print("\n" + "-" * 80)
