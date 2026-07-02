from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UploadReportRequest(BaseModel):
    pass


class ReportResponse(BaseModel):
    id: UUID
    user_id: UUID

    original_file_name: str
    stored_file_name: str

    file_type: str
    file_size: int

    storage_path: str

    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReportListResponse(BaseModel):
    reports: list[ReportResponse]