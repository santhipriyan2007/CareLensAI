from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class HistoryItem(BaseModel):
    """
    Represents a single AI analysis history record.
    """

    analysis_id: UUID
    report_id: UUID

    report_name: str

    risk_level: str
    urgency: str

    confidence_score: int = Field(
        ge=0,
        le=100,
    )

    analysis_date: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class HistoryResponse(BaseModel):
    """
    Paginated analysis history response.
    """

    page: int

    page_size: int

    total: int

    total_pages: int

    items: list[HistoryItem]