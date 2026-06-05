from src.rag.retrieval import retrieve_chunks


results = retrieve_chunks("What is llm?")

print("\nRetrieved Chunks:\n")

for result in results:
    print(result.page_content[:500])

    print("\n---\n")
