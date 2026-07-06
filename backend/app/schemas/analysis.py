from datetime import datetime
from typing import Any

from pydantic import BaseModel
from uuid import UUID


class AnalysisResponse(BaseModel):
    id: UUID
    report_id: UUID
    analysis: dict[str, Any]
    created_at: datetime


class AnalysisCreateResponse(BaseModel):
    message: str
    analysis: AnalysisResponse