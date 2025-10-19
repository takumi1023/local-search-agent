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

from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.llms import OpenAI

from .config import settings

# Load embeddings and vector store
embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
db = Chroma(
    persist_directory=".chroma",
    embedding_function=embeddings,
    collection_name=settings.collection_name
)
retriever = db.as_retriever(search_kwargs={"k": 5})

# Create QA chain
qa = RetrievalQA.from_chain_type(
    llm=OpenAI(model_name="gpt-3.5-turbo", openai_api_key=settings.openai_api_key),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
)

# Query function
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
