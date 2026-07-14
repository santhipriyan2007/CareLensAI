from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import require_role
from app.schemas.history import HistoryResponse
from app.services.history_service import HistoryService

router = APIRouter(
    prefix="/analysis/history",
    tags=["Analysis History"],
)


@router.get(
    "",
    response_model=HistoryResponse,
)
def get_analysis_history(
    page: int = Query(
        default=1,
        ge=1,
        description="Page number",
    ),
    page_size: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of records per page",
    ),
    report_id: UUID | None = Query(
        default=None,
        description="Filter by report ID",
    ),
    start_date: date | None = Query(
        default=None,
        description="Filter analyses from this date",
    ),
    end_date: date | None = Query(
        default=None,
        description="Filter analyses until this date",
    ),
    current_user=Depends(require_role("doctor")),
):
    """
    Retrieve paginated AI analysis history.
    """

    return HistoryService.get_history(
        page=page,
        page_size=page_size,
        report_id=report_id,
        start_date=start_date,
        end_date=end_date,
    )