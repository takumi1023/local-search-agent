import streamlit as st
from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.callbacks.base import BaseCallbackHandler
from config import settings
import gc

# =========================
# Page Setup
# =========================
st.set_page_config(page_title="Local Search Agent", page_icon="🧠", layout="wide")
st.markdown("""
<style>
/* Chat bubbles */
.user-bubble {
    background-color: #DCF8C6;
    padding: 10px;
    border-radius: 15px;
    margin-bottom: 5px;
    max-width: 80%;
    text-align: left;
}
.ai-bubble {
    background-color: #F1F0F0;
    padding: 10px;
    border-radius: 15px;
    margin-bottom: 5px;
    max-width: 80%;
    text-align: left;
}
.chat-container {
    display: flex;
    flex-direction: column;
}
.user-container {
    align-items: flex-end;
    display: flex;
}
.ai-container {
    align-items: flex-start;
    display: flex;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 Local Search Agent")

# =========================
# Initialize session state
# =========================
if "history" not in st.session_state:
    st.session_state.history = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

gc.collect()

# =========================
# Streaming callback for Streamlit
# =========================
class StreamlitCallbackHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""
    
    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)

# =========================
# Initialize LLM and QA chain once
# =========================
st.sidebar.header("🔧 System Status")
try:
    if "llm" not in st.session_state:
        st.session_state.llm = OllamaLLM(
            model=settings.ollama_model,
            callbacks=[],
            verbose=True
        )

    if "qa_chain" not in st.session_state:
        embeddings = OllamaEmbeddings(model=settings.ollama_model)
        db = Chroma(
            persist_directory=".chroma",
            embedding_function=embeddings,
            collection_name=settings.collection_name
        )
        retriever = db.as_retriever(search_kwargs={"k": 2})

        st.session_state.qa_chain = RetrievalQA.from_chain_type(
            llm=st.session_state.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )

        # Show DB info
        try:
            num_docs = len(db._collection.get()['documents'])
            st.sidebar.success("✅ Connected to ChromaDB")
            st.sidebar.write(f"Documents in '{settings.collection_name}': {num_docs}")
        except Exception:
            st.sidebar.warning("⚠️ Could not read documents from ChromaDB")

except Exception as e:
    st.sidebar.error("❌ Failed to connect to ChromaDB")
    st.sidebar.write(e)
    st.stop()

# =========================
# Submit query function
# =========================
def submit_query():
    query = st.session_state.input_text.strip()
    if not query:
        return

    # Placeholder for streaming
    container = st.empty()
    handler = StreamlitCallbackHandler(container)

    # Attach callback
    st.session_state.llm.callbacks = [handler]

    # Run QA chain with invoke
    try:
        result = st.session_state.qa_chain.invoke({"query": query})
        answer_text = result["result"]
        # source_docs = result.get("source_documents", [])
    except Exception as e:
        st.error(f"❌ Error during query: {e}")
        st.session_state.input_text = ""
        return

    # Save history
    st.session_state.history.append({
        "query": query,
        "answer": answer_text,
        # "sources": source_docs
    })

    st.session_state.input_text = ""  # clear input

# =========================
# Chat history with bubbles
# =========================
st.markdown("### 💬 Chat History")
for item in st.session_state.history:
    # User bubble
    st.markdown(f"""
    <div class="chat-container">
        <div class="user-container">
            <div class="user-bubble"><b>You:</b> {item['query']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # AI bubble
    st.markdown(f"""
    <div class="chat-container">
        <div class="ai-container">
            <div class="ai-bubble"><b>AI:</b> {item['answer']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Source documents
    # if item.get("sources"):
    #     for j, doc in enumerate(item["sources"], 1):
    #         with st.expander(f"Document {j}"):
    #             st.write(doc.page_content)
    #             st.caption(f"Metadata: {doc.metadata}")
    st.markdown("---")

# =========================
# Input box at the bottom
# =========================
st.text_input(
    "Type your question here and press Enter:",
    key="input_text",
    on_change=submit_query,
    placeholder="e.g. What is LangChain?"
)





# import streamlit as st
# from langchain.chains import RetrievalQA
# from langchain_chroma import Chroma
# from langchain_ollama import OllamaEmbeddings, OllamaLLM
# from config import settings
# import gc

# # =========================
# # Page Setup
# # =========================
# st.set_page_config(page_title="Local Search Agent", page_icon="🧠", layout="wide")
# st.title("🧠 Local Search Agent")
# st.caption("Ask questions about your local knowledge base using Ollama + ChromaDB")

# # =========================
# # Initialize chat history in session state
# # =========================
# if "history" not in st.session_state:
#     st.session_state.history = []

# if "input_text" not in st.session_state:
#     st.session_state.input_text = ""

# # =========================
# # Clean up previous runs
# # =========================
# gc.collect()

# # =========================
# # Load Embeddings & ChromaDB
# # =========================
# st.sidebar.header("🔧 System Status")
# try:
#     embeddings = OllamaEmbeddings(model=settings.ollama_model)
#     db = Chroma(
#         persist_directory=".chroma",
#         embedding_function=embeddings,
#         collection_name=settings.collection_name
#     )

#     retriever = db.as_retriever(search_kwargs={"k": 2})
#     qa = RetrievalQA.from_chain_type(
#         llm=OllamaLLM(model=settings.ollama_model),
#         chain_type="stuff",
#         retriever=retriever,
#         return_source_documents=True
#     )

#     # Check number of documents
#     try:
#         num_docs = len(db._collection.get()['documents'])
#         st.sidebar.success("✅ Connected to ChromaDB")
#         st.sidebar.write(f"Documents in '{settings.collection_name}': {num_docs}")
#     except Exception:
#         st.sidebar.warning("⚠️ Could not read documents from ChromaDB")

# except Exception as e:
#     st.sidebar.error("❌ Failed to connect to ChromaDB")
#     st.sidebar.write(e)
#     st.stop()

# # =========================
# # User Input
# # =========================
# def submit_query():
#     query = st.session_state.input_text.strip()
#     if not query:
#         return
#     if query.lower() == "exit":
#         st.warning("⚠️ Streamlit GUI does not need 'exit'. Just refresh or close the browser.")
#         st.session_state.input_text = ""
#         return

#     with st.spinner("🔍 Searching the knowledge base..."):
#         try:
#             result = qa.invoke({"query": query})
#         except Exception as e:
#             st.error(f"❌ Error during query: {e}")
#             st.session_state.input_text = ""
#             return

#     # Save question + answer to history
#     st.session_state.history.append({
#         "query": query,
#         "answer": result["result"],
#         "sources": result.get("source_documents", [])
#     })

#     # Clear input box
#     st.session_state.input_text = ""

# st.text_input(
#     "Type your question below and press Enter:",
#     key="input_text",
#     on_change=submit_query,
#     placeholder="e.g. What is LangChain?"
# )

# # =========================
# # Display Chat History
# # =========================
# st.markdown("### 💬 Chat History")

# for i, item in enumerate(st.session_state.history):
#     st.markdown(f"**You:** {item['query']}")
#     st.markdown(f"**AI:** {item['answer']}")
#     # if item["sources"]:
#     #     for j, doc in enumerate(item["sources"], 1):
#     #         with st.expander(f"Document {j}"):
#     #             st.write(doc.page_content)
#     #             st.caption(f"Metadata: {doc.metadata}")
#     st.markdown("---")
