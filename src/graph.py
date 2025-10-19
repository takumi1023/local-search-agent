from typing import Dict, Any, List

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langgraph.graph import StateGraph, START, END

from .config import settings


class AgentState(dict):
    query: str
    retrieved: List[Document]
    summary: str


def build_retriever(persist_dir: str, collection: str):
    embeddings = OllamaEmbeddings(model=settings.ollama_model)
    vectordb = Chroma(
        embedding_function=embeddings,
        persist_directory=persist_dir,
        collection_name=collection,
    )
    return vectordb.as_retriever(search_kwargs={"k": 5})


def node_input_handler(state: AgentState) -> AgentState:
    # passthrough; can normalize or validate
    return state


def node_retriever(state: AgentState) -> AgentState:
    retriever = build_retriever(settings.chroma_dir, settings.collection_name)
    docs = retriever.get_relevant_documents(state["query"])  # type: ignore
    state["retrieved"] = docs
    return state


def node_summarizer(state: AgentState) -> AgentState:
    llm = ChatOllama(model=settings.ollama_model)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful research assistant. Summarize the provided context to answer the user question concisely. If unsure, say you don't know."),
        ("human", "Question: {question}\n\nContext chunks:\n{context}\n\nProvide a concise, well-structured answer."),
    ])
    context = "\n\n".join(
        [f"[Source: {d.metadata.get('source','unknown')}]\n{d.page_content}" for d in state.get("retrieved", [])]
    )
    chain = prompt | llm
    response = chain.invoke({"question": state["query"], "context": context})
    state["summary"] = response.content if hasattr(response, "content") else str(response)
    return state


def node_output_formatter(state: AgentState) -> AgentState:
    # Could add citations or formatting here; pass through for CLI to render
    return state


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("input", node_input_handler)
    graph.add_node("retrieve", node_retriever)
    graph.add_node("summarize", node_summarizer)
    graph.add_node("format", node_output_formatter)

    graph.add_edge(START, "input")
    graph.add_edge("input", "retrieve")
    graph.add_edge("retrieve", "summarize")
    graph.add_edge("summarize", "format")
    graph.add_edge("format", END)

    return graph.compile()

