from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.core.dependencies import get_current_user, require_role
from app.schemas.report import ReportListResponse, ReportResponse
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
    patient_user_id: UUID = Form(...),
    file: UploadFile = File(...),
    current_user: UserResponse = Depends(require_role("doctor")),
):
    """
    Upload a medical report for a patient.
    """

    return await ReportService.create_report(
        file=file,
        patient_user_id=patient_user_id,
        uploaded_by_user_id=current_user.id,
    )


@router.get(
    "",
    response_model=ReportListResponse,
)
async def get_reports(
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Retrieve reports.
    """

    return await ReportService.get_reports(current_user)


@router.get(
    "/{report_id}",
    response_model=ReportResponse,
)
async def get_report(
    report_id: UUID,
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Retrieve a single report.
    """

    return await ReportService.get_report_by_id(
        report_id=report_id,
        current_user=current_user,
    )


@router.get(
    "/{report_id}/signed-url",
)
async def get_signed_url(
    report_id: UUID,
    current_user: UserResponse = Depends(get_current_user),
):
    """
    Generate a temporary signed URL
    for a medical report.
    """

    return await ReportService.get_signed_url(
        report_id=report_id,
        current_user=current_user,
    )