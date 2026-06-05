from src.rag_pipeline import process_query

print("Vector database loaded successfully")

# CHAT LOOP STARTS HERE
if __name__ == "__main__":
    while True:
        # Ask user question
        query = input("\nAsk your question: ")

        # Exit chatbot
        if query.lower() == "exit":
            print("Exiting chatbot...")
            break

        # Use shared RAG function
        answer, sources = process_query(query)

        print("\nAnswer:\n")
        print(answer)

        # Print citations ONLY if answer was found
        if "I could not find" not in answer:
            print("\nSources:\n")
            print(sources)
