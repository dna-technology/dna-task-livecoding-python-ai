from __future__ import annotations
from pathlib import Path
from typing import List
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.schema import Document
from .config import settings

_PROMPT = PromptTemplate(
    template=(
        "You are a helpful assistant.\n"
        "Answer the *exact* question using ONLY the context below. If the answer is not"
        " contained in the context, say 'I don't know'.\n\n"
        "Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    ),
    input_variables=["context", "question"],
)


def _load_vector_store() -> FAISS:
    """Load FAISS index once and cache in-memory."""
    if not settings.vector_dir.exists():
        raise FileNotFoundError("Vector store not found. Have you ingested any documents yet?")
    embeddings = OpenAIEmbeddings(model=settings.embeddings_model, api_key=settings.openai_api_key)
    return FAISS.load_local(
        str(settings.vector_dir), embeddings, allow_dangerous_deserialization=True
    )


def _retrieve(filename: str, question: str, k: int = 4) -> List[Document]:
    """Vector similarity search then metadata filter by source filename."""

    vs = _load_vector_store()

    candidates = vs.similarity_search(question, k=15)
    docs = [d for d in candidates if d.metadata.get("source") == filename][:k]

    if len(docs) < k:
        docs = candidates[:k]

    return docs

def answer_question(filename: str, question: str) -> str:
    """Main entry – used by FastAPI layer and notebooks."""

    pdf_path = Path(settings.data_dir) / filename
    if not pdf_path.exists():
        raise FileNotFoundError(pdf_path)

    docs = _retrieve(filename, question)
    context = "\n---\n".join(d.page_content for d in docs)

    llm = ChatOpenAI(model_name=settings.model_name, temperature=0, api_key=settings.openai_api_key)
    response = llm.invoke(_PROMPT.format(context=context, question=question))
    return response.content 