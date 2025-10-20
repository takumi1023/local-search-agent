# # app/query.py

# from langchain.chains import RetrievalQA
# from langchain.vectorstores import Chroma
# from langchain.embeddings import OllamaEmbeddings
# from langchain.llms import Ollama

# from .config import settings

# # Load embeddings
# embeddings = OllamaEmbeddings(model=settings.ollama_model)

# # Create vector store (fresh directory to avoid corrupted collection errors)
# db = Chroma(
#     persist_directory="/tmp/chroma",  # temporary directory in Render container
#     embedding_function=embeddings,
#     collection_name=settings.collection_name
# )
# retriever = db.as_retriever(search_kwargs={"k": 5})

# # Create QA chain
# qa = RetrievalQA.from_chain_type(
#     llm=Ollama(model=settings.ollama_model),
#     chain_type="stuff",
#     retriever=retriever,
#     return_source_documents=True,
# )

# # Query function
# def query_chroma(query_text):
#     result = qa.invoke({"query": query_text})
#     return result["result"]

# # Interactive loop if executed directly
# if __name__ == "__main__":
#     while True:
#         query = input("\nEnter your question (or 'exit' to quit): ")
#         if query.lower() == "exit":
#             break
#         print("Searching...")
#         answer = query_chroma(query)
#         print("\nAnswer:", answer)


# app/query.py

# app/query.py

# from langchain.chains import RetrievalQA
# from langchain_chroma import Chroma
# from langchain_ollama import OllamaEmbeddings, OllamaLLM

# from .config import settings

# # Load embeddings and vector store
# embeddings = OllamaEmbeddings(model=settings.ollama_model)
# db = Chroma(
#     persist_directory=".chroma",
#     embedding_function=embeddings,
#     collection_name=settings.collection_name
# )
# retriever = db.as_retriever(search_kwargs={"k": 5})

# # Create QA chain
# qa = RetrievalQA.from_chain_type(
#     llm=OllamaLLM(model=settings.ollama_model),
#     chain_type="stuff",
#     retriever=retriever,
#     return_source_documents=True,
# )

# def query_chroma(query_text: str):
#     result = qa.invoke({"query": query_text})
#     return result["result"]

# if __name__ == "__main__":
#     while True:
#         query = input("\nEnter your question (or 'exit' to quit): ")
#         if query.lower() == "exit":
#             break
#         print("Searching...")
#         answer = query_chroma(query)
#         print("\nAnswer:", answer)


# app/query.py
from langchain.chains import RetrievalQA
from langchain.vectorstores import Chroma
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.llms import GPT4All
import os

# -----------------------------
# 1. Free embeddings
# -----------------------------
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# -----------------------------
# 2. Load Chroma vector DB (local)
# -----------------------------
persist_directory = os.path.join(os.getcwd(), "db")
db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

# -----------------------------
# 3. Create retriever
# -----------------------------
retriever = db.as_retriever(search_kwargs={"k": 3})

# -----------------------------
# 4. Free local LLM (GPT4All)
# -----------------------------
llm_model_path = os.path.join(os.getcwd(), "models", "gpt4all-lora-quantized.bin")
llm = GPT4All(model=llm_model_path, verbose=False)

qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

# -----------------------------
# 5. Query function
# -----------------------------
def query_chroma(query_text: str):
    try:
        result = qa.run(query_text)
        return result
    except Exception as e:
        return f"Error: {str(e)}"
