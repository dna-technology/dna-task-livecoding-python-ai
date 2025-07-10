from __future__ import annotations
from pathlib import Path
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from .config import settings

def main(pdf_path: Path) -> None:
    """Idempotently ingest *one* PDF.

    Steps:
    1. parse PDF → LangChain Documents
    2. chunk (RecursiveCharacterTextSplitter)
    3. embed + store in FAISS with metadata
    """

    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)

    # 1️⃣ Parse PDF
    loader = PyPDFLoader(str(pdf_path))  # ↔ switch to UnstructuredPDFLoader for OCR
    pages: List[Document] = loader.load()

    # 2️⃣ Chunk
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap
    )
    chunks: List[Document] = splitter.split_documents(pages)

    # 3️⃣ Embeddings & vector DB
    embeddings = OpenAIEmbeddings(model=settings.embeddings_model, api_key=settings.openai_api_key)

    # Tag chunks with source filename (helps retrieval filtering)
    for c in chunks:
        c.metadata["source"] = pdf_path.name

    if settings.vector_dir.exists():
        vector_store = FAISS.load_local(
            str(settings.vector_dir), embeddings, allow_dangerous_deserialization=True
        )
        vector_store.add_documents(chunks)
    else:
        vector_store = FAISS.from_documents(chunks, embeddings)

    settings.vector_dir.mkdir(parents=True, exist_ok=True)
    vector_store.save_local(str(settings.vector_dir))

    print(f"✓ Ingested {pdf_path.name} ({len(chunks)} chunks)")
