from pydantic import BaseModel


class OCRResponse(BaseModel):
    """
    Response returned after OCR extraction.
    """

    success: bool
    message: str
    extracted_text: str