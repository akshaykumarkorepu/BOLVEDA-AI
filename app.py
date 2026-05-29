from dotenv import load_dotenv

# Import custom modules
from src.pdf_loader import load_pdf
from src.chunking import create_chunks
from src.embeddings import create_vector_store

# Load .env variables
load_dotenv()

# PDF file path
pdf_path = "data/sample.pdf"

# Step 1: Load PDF
documents = load_pdf(pdf_path)

print("PDF loaded successfully")

# Step 2: Create chunks
chunks = create_chunks(documents)

print("Chunks created successfully")

# Step 3: Create vector database
vector_store = create_vector_store(chunks)

print("Vector database created successfully")
