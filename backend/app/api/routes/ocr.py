from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.schemas.ocr import OCRResponse
from app.services.ocr_service import OCRService

router = APIRouter(
    prefix="/ocr",
    tags=["OCR"],
)


@router.post(
    "/extract",
    response_model=OCRResponse,
)
async def extract_text(
    file: UploadFile = File(...),
):
    """
    Extract text from an uploaded medical report.
    """

    try:

        extracted_text = (
            await OCRService.extract_text_from_upload(
                file
            )
        )

        return OCRResponse(
            success=True,
            message="OCR completed successfully.",
            extracted_text=extracted_text,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )