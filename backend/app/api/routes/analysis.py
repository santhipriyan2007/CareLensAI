from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.core.dependencies import (
    get_current_user,
    require_role,
)
from app.schemas.analysis import AnalysisCreateResponse
from app.schemas.user import UserResponse
from app.services.analysis_service import AnalysisService

router = APIRouter(
    prefix="/analysis",
    tags=["AI Analysis"],
)

analysis_service = AnalysisService()


@router.post(
    "/report/{report_id}",
    response_model=AnalysisCreateResponse,
    status_code=status.HTTP_200_OK,
)
def analyze_report(
    report_id: UUID,
    current_user: UserResponse = Depends(
        require_role("doctor")
    ),
):
    """
    Analyze an uploaded medical report using OCR + Gemini AI.
    """

    return analysis_service.analyze_report(
        report_id
    )