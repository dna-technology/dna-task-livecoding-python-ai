from pathlib import Path
from fastapi import APIRouter, HTTPException, status

from .schemas import IngestRequest, AskRequest, AskResponse
from ..config import settings
from ..ingest import main as ingest_main
from ..rag import answer_question

router = APIRouter(prefix="", tags=["RAG"])

@router.post("/ingest", status_code=status.HTTP_201_CREATED)
def ingest(req: IngestRequest):
    """Parse + embed a PDF. Idempotent – safe to call multiple times."""

    pdf_path = Path(settings.data_dir) / req.filename
    try:
        ingest_main(pdf_path)
    except Exception as exc:  # noqa: BLE001 – want to catch all for demo
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {"status": "ok"}

@router.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    """Run RAG over a previously-ingested file."""

    try:
        answer = answer_question(req.filename, req.question)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return AskResponse(answer=answer) 

