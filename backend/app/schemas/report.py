from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UploadReportRequest(BaseModel):
    pass


class ReportResponse(BaseModel):
    id: UUID

    patient_user_id: UUID
    uploaded_by_user_id: UUID

    original_file_name: str
    file_type: str
    file_size: int

    uploaded_at: datetime

    download_url: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ReportListResponse(BaseModel):
    total: int
    reports: list[ReportResponse]