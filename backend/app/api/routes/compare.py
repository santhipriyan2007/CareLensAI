from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.dependencies import require_role
from app.schemas.compare import CompareReportsResponse
from app.services.compare_service import CompareService

router = APIRouter(
    prefix="/compare",
    tags=["Compare Reports"],
)


@router.get(
    "",
    response_model=CompareReportsResponse,
    summary="Compare two medical reports",
)
def compare_reports(
    previous_report_id: UUID,
    current_report_id: UUID,
    _: object = Depends(require_role("doctor")),
):
    """
    Retrieve two analysed reports that will
    be compared in later milestones.
    """

    return CompareService.get_reports_for_comparison(
        previous_report_id=previous_report_id,
        current_report_id=current_report_id,
    )