from uuid import UUID

from fastapi import APIRouter, Depends

from app.core.dependencies import require_role
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.user import UserResponse
from app.services.chat_service import ChatService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    current_user: UserResponse = Depends(
        require_role("doctor")
    ),
) -> ChatResponse:
    """
    Answer a doctor question using a medical report
    as the retrieval source.
    """

    return await ChatService.chat(
        report_id=request.report_id,
        question=request.question,
        current_user=current_user,
    )