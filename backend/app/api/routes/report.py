from fastapi import APIRouter, Depends, File, UploadFile
from app.schemas.report import ReportResponse

from app.core.dependencies import require_role
from app.schemas.user import UserResponse
from app.services.report_service import ReportService

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.post(
    "/upload",
    response_model=ReportResponse,
)
async def upload_report(
    file: UploadFile = File(...),
    current_user: UserResponse = Depends(require_role("doctor")),
):

    report = await ReportService.create_report(
        file=file,
        user_id=current_user.id,
    )

    return report