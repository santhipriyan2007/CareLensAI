from uuid import UUID

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Request payload for report-aware AI medical chat.
    """

    report_id: UUID

    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
    )


class ChatResponse(BaseModel):
    """
    Response returned by the AI medical chat service.
    """

    report_id: UUID
    question: str
    answer: str
    medical_disclaimer: str