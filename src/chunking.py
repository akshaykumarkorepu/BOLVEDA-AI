from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Path to PDF
pdf_path = "data/sample.pdf"

# Create PDF loader
loader = PyPDFLoader(pdf_path)

# Load PDF pages
documents = loader.load()

# Print total pages
print(f"\nTotal pages loaded: {len(documents)}\n")

# Create text splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Split documents into chunks
chunks = text_splitter.split_documents(documents)

# Print total chunks
print(f"\nTotal chunks created: {len(chunks)}\n")

# Print second chunk
print("\nSECOND CHUNK\n")
print(chunks[1].page_content)

# Print metadata
print("\nCHUNK METADATA:\n")
print(chunks[1].metadata)

# Debug first 5 chunks
for i, chunk in enumerate(chunks[:5]):
    print(f"\nCHUNK {i + 1}\n")

    print(chunk.page_content)

    print("\n" + "-" * 80)
