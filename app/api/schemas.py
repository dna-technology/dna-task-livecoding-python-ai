from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    """Body for `/ingest` – provide a filename located under `data/documents/`."""

    filename: str = Field(..., examples=["my_report.pdf"])


class AskRequest(BaseModel):
    """Body for `/ask` – ask about a known document."""

    filename: str = Field(..., examples=["my_report.pdf"])
    question: str = Field(..., examples=["What is the executive summary?"])


class AskResponse(BaseModel):
    """Answer wrapper – ready for further metadata (sources, cost, etc.)."""

    answer: str 