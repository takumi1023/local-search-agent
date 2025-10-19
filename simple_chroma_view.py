from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

# Load ChromaDB
embeddings = OllamaEmbeddings(model='llama3')
db = Chroma(persist_directory='.chroma', embedding_function=embeddings, collection_name='local-research-agent')

# Get all documents
docs = db.get()

print(f"Total documents in ChromaDB: {len(docs['documents'])}")
print("\nSource files:")
sources = set(doc['source'] for doc in docs['metadatas'])
for source in sources:
    print(f"  - {source}")

print("\nFirst 5 documents:")
for i in range(min(16, len(docs['documents']))):
    print(f"\nDocument {i+1}:")
    print(f"  Source: {docs['metadatas'][i]['source']}")
    print(f"  Content: {docs['documents'][i][:150]}...")
