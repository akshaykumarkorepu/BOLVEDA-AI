from src.rag.rag_pipeline import process_query


print("\nTesting Full RAG Pipeline:\n")


for chunk, citation in process_query("What is llm?"):
    # Stream response chunks
    if chunk:
        print(chunk, end="")

    # Print citations at end
    if citation:
        print("\n\nSources:")
        print(citation)
