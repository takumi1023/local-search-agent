from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

# Initialize embeddings and Chroma
embeddings = OllamaEmbeddings(model='llama3')
db = Chroma(
    persist_directory='.chroma',
    embedding_function=embeddings,
    collection_name='local-research-agent'
)

# Load all documents
docs = db.get()

print(f"Total documents in ChromaDB: {len(docs['documents'])}")
if len(docs['documents']) == 0:
    print("No documents found.")
    exit()

# Show available sources
print("\nSource files:")
sources = set(doc['source'] for doc in docs['metadatas'])
for source in sources:
    print(f"  - {source}")

# Show first few documents for preview
print("\nPreview (first 5 documents):")
for i in range(min(5, len(docs['documents']))):
    print(f"\nDocument ID: {docs['ids'][i]}")
    print(f"Source: {docs['metadatas'][i]['source']}")
    print(f"Content: {docs['documents'][i][:150]}...")

# Ask user for action
choice = input("\nEnter a source name or document ID to delete (or press Enter to cancel): ").strip()

if choice:
    # Try to match by source name first
    matched_ids = [docs['ids'][i] for i, m in enumerate(docs['metadatas']) if m.get('source') == choice]

    if not matched_ids:
        # If not found by source, maybe user gave an ID
        if choice in docs['ids']:
            matched_ids = [choice]

    if matched_ids:
        print(f"\nDeleting {len(matched_ids)} document(s): {matched_ids}")
        db.delete(ids=matched_ids)
        print("Deleted successfully.")
    else:
        print("No documents found matching that source or ID.")
else:
    print("Cancelled. No changes made.")