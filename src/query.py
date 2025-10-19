from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama import OllamaLLM

from .config import settings

# Load embeddings and vector store
embeddings = OllamaEmbeddings(model=settings.ollama_model)
db = Chroma(persist_directory=".chroma", embedding_function=embeddings, collection_name=settings.collection_name)
retriever = db.as_retriever(search_kwargs={"k": 5})

# Create QA chain
qa = RetrievalQA.from_chain_type(
    llm=OllamaLLM(model=settings.ollama_model),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
)

# Query loop
while True:
    query = input("\nEnter your question (or 'exit' to quit): ")
    if query.lower() == "exit":
        break
    print("Searching...")
    result = qa.invoke({"query": query})
    print("\nAnswer:", result["result"])


def query_chroma(query_text):
    # your existing Chroma logic here
    return "Sample result for: " + query_text

