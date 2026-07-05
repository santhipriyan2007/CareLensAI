import os
import tempfile
from pathlib import Path

from fastapi import UploadFile

from app.ocr.easyocr_engine import EasyOCREngine
from app.ocr.image_preprocessor import ImagePreprocessor
from app.ocr.pdf_processor import PDFProcessor
from app.ocr.text_cleaner import TextCleaner


class OCRService:
    """
    Service responsible for extracting text
    from medical reports.
    """

    @staticmethod
    async def extract_text_from_upload(
        file: UploadFile,
    ) -> str:
        """
        Complete OCR pipeline starting from an uploaded file.
        """

        suffix = Path(file.filename).suffix

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp_file:

            temp_file.write(await file.read())
            temp_path = temp_file.name

        try:
            return OCRService.extract_text_from_pdf(
                temp_path
            )

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    @staticmethod
    def extract_text_from_pdf(
        pdf_path: str,
    ) -> str:
        """
        Complete OCR pipeline.

        PDF
            ↓
        Images
            ↓
        Preprocess
            ↓
        EasyOCR
            ↓
        Clean Text
        """

        images = PDFProcessor.convert_pdf_to_images(
            pdf_path
        )

        extracted_pages = []

        for image in images:

            processed = ImagePreprocessor.preprocess(
                image
            )

            text = OCRService._extract_text(
                processed
            )

            cleaned = TextCleaner.clean(
                text
            )

            extracted_pages.append(
                cleaned
            )

        return "\n\n".join(extracted_pages)

    @staticmethod
    def _extract_text(image):
        """
        Internal OCR abstraction.

        Currently uses EasyOCR.
        Can later be upgraded to:
        - EasyOCR + Tesseract
        - Google Vision
        - PaddleOCR
        """

        return EasyOCREngine.extract_text(image)