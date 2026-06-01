from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

embedding_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")

vector_store = Chroma(persist_directory="chroma_db", embedding_function=embedding_model)


def retrieve_chunks(query, k=3):
    results = vector_store.similarity_search(query, k=k)

    return results
