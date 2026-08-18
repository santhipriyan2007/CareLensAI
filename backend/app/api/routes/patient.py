from fastapi import APIRouter, Depends

from app.core.dependencies import require_role
from app.schemas.user import UserResponse
from app.services.patient_service import PatientService


router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)


@router.get(
    "",
    response_model=list[UserResponse],
)
async def get_patients(
    current_user=Depends(require_role("doctor")),
):
    """
    Retrieve patients for doctor report assignment.
    """

    return await PatientService.get_patients()