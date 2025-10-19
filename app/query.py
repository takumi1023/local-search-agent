# app/query.py

from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM

from .config import settings

# Load embeddings and vector store
embeddings = OllamaEmbeddings(model=settings.ollama_model)
db = Chroma(
    persist_directory=".chroma",
    embedding_function=embeddings,
    collection_name=settings.collection_name
)
retriever = db.as_retriever(search_kwargs={"k": 5})

# Create QA chain
qa = RetrievalQA.from_chain_type(
    llm=OllamaLLM(model=settings.ollama_model),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
)

# Query function (safe to import)
def query_chroma(query_text):
    result = qa.invoke({"query": query_text})
    return result["result"]

# Only run interactive loop if executed directly
if __name__ == "__main__":
    while True:
        query = input("\nEnter your question (or 'exit' to quit): ")
        if query.lower() == "exit":
            break
        print("Searching...")
        answer = query_chroma(query)
        print("\nAnswer:", answer)
