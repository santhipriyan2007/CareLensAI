import os
import tempfile
from pathlib import Path

from fastapi import UploadFile

from app.ocr.easyocr_engine import EasyOCREngine
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
        Complete text extraction pipeline starting
        from an uploaded file.

        For PDF files:
        1. Try native PDF text extraction.
        2. Fall back to OCR when native text is unavailable.

        The temporary file is removed after processing.
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
        Hybrid PDF text extraction pipeline.

        PDF
            ↓
        Native text extraction
            ↓
        Usable text?
          ├── Yes → Clean Text → Return
          └── No  → Images → EasyOCR
                              → Clean Text → Return
        """

        native_text = PDFProcessor.extract_native_text(
            pdf_path
        )

        if PDFProcessor.has_usable_native_text(
            native_text
        ):
            return TextCleaner.clean(
                native_text
            )

        return OCRService._extract_text_with_ocr(
            pdf_path
        )

    @staticmethod
    def _extract_text_with_ocr(
        pdf_path: str,
    ) -> str:
        """
        OCR fallback for scanned/image-based PDFs.

        The original 300-DPI image is passed directly
        to EasyOCR for this OCR quality test.

        Image preprocessing is intentionally bypassed
        here temporarily so that OCR performance can be
        compared against the previous preprocessing pipeline.
        """

        images = PDFProcessor.convert_pdf_to_images(
            pdf_path
        )

        extracted_pages = []

        for image in images:

            text = OCRService._extract_text(
                image
            )

            cleaned = TextCleaner.clean(
                text
            )

            extracted_pages.append(
                cleaned
            )

        return "\n\n".join(
            extracted_pages
        )

    @staticmethod
    def _extract_text(
        image,
    ) -> str:
        """
        Internal OCR abstraction.

        Currently uses EasyOCR.

        Can later be upgraded to:
        - EasyOCR + Tesseract
        - Google Vision
        - PaddleOCR
        """

        return EasyOCREngine.extract_text(
            image
        )

