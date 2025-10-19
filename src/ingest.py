import argparse
from pathlib import Path
from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

from .config import settings

def load_documents(data_dir: str) -> List:
    loaders = [
        DirectoryLoader(data_dir, glob="**/*.md", loader_cls=TextLoader, show_progress=True),
        DirectoryLoader(data_dir, glob="**/*.txt", loader_cls=TextLoader, show_progress=True),
    ]
    docs = []
    for loader in loaders:
        docs.extend(loader.load())
    return docs


def ingest(data_dir: str, persist_dir: str, collection: str) -> None:
    docs = load_documents(data_dir)
    if not docs:
        print("No documents found. Place .md or .txt files in the data directory.")
        return

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        add_start_index=True,
    )
    chunks = splitter.split_documents(docs)

    embeddings = OllamaEmbeddings(model=settings.ollama_model)

    Chroma.from_documents(
        chunks,
        embedding=embeddings,
        persist_directory=persist_dir,
        collection_name=collection,
    )
    print(f"Ingestion complete. Persisted to: {persist_dir} (collection: {collection})")

def main():
    parser = argparse.ArgumentParser(description="Ingest local documents into Chroma.")
    parser.add_argument("--data-dir", default=settings.data_dir, help="Directory with .md/.txt files")
    parser.add_argument("--persist-dir", default=settings.chroma_dir, help="Chroma persistence directory")
    parser.add_argument("--collection", default=settings.collection_name, help="Chroma collection name")
    args = parser.parse_args()

    Path(args.persist_dir).mkdir(parents=True, exist_ok=True)
    ingest(args.data_dir, args.persist_dir, args.collection)


if __name__ == "__main__":
    main()

