# Simple RAG – Learning Playground

This mini-project demonstrates a ** Retrieval-Augmented-Generation (RAG)** application using modern tooling:

- [FastAPI](https://fastapi.tiangolo.com) – production-ready HTTP interface
- [LangChain](https://python.langchain.com) – document loading, chunking, vector store and LLM helpers
- [OpenAI](https://platform.openai.com) – GPT family models for embedding + generation
- [FAISS](https://github.com/facebookresearch/faiss) – lightweight vector DB

---

## Quick-start (local)

```bash
# 1. install deps
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. set your OpenAI key in .env file
OPENAI_API_KEY="sk-..."

# 3. add a PDF to data/documents/ or reuse the existing ones
mkdir -p data/documents && cp ~/Downloads/my.pdf data/documents/

# 4. run the API
python scripts/run_server.py
```

Play with it (e.g. using `curl` or [Hoppscotch](https://hoppscotch.io)):

```bash
# A) build the vector store for the PDF (idempotent)
curl -X POST localhost:8000/ingest -H "Content-Type: application/json" \
     -d '{"filename": "financial-summary-rag.pdf"}'

# B) ask a question
curl -X POST localhost:8000/ask -H "Content-Type: application/json" \
     -d '{"filename": "financial-summary-rag.pdf", "question": "What is the total revenue of Acme Corp for Q2 2025?"}'

# or

curl -X POST localhost:8000/ask -H "Content-Type: application/json" \
     -d '{"filename": "financial-summary-rag.pdf", "question": "Debt-to-equity ratio of Beta Tech?"}'

# or

curl -X POST localhost:8000/ask -H "Content-Type: application/json" \
     -d '{"filename": "financial-summary-rag.pdf", "question": "What is the management outlook for growth?"}'
```

---

## Questions & Suggestions

1. Should we keep the ingest and ask endpoints separate or maybe prepare a single endpoint and see if the candidate sees a room for improvement?
2. Tightly coupled with Langchain for now - do we want to move some logic out of the LangChain tools?
3. The pipeline now works properly - we should probably break it in some places to let the candidate fix and show their skills.
4. We could add more documents for testing.
5. The prompt in rag.py should be simplified to complete basics so that the candidate shows understanding of prompt engineering.
