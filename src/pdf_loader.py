from langchain_community.document_loaders import PyPDFLoader

# Path to the PDF
pdf_path = "data/sample.pdf"

# Creating PDF loader
loader = PyPDFLoader(pdf_path)

# Load PDF
documents = loader.load()

# Print total pages
print(f"\nTotal pages loaded:{len(documents)}\n")

# Print the 1st page content

print("\nSECOND PAGE CONTENT:\n")

print(documents[1].page_content)

# Print metadata

print("\nMETADATA:\n")

print(documents[1].metadata)

# Debug all pages
for i, doc in enumerate(documents):
    print(f"\nPAGE {i + 1}\n")

    print(doc.page_content[:500])
