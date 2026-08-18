from pathlib import Path

import cv2
import numpy as np
import fitz
from pdf2image import convert_from_path

from app.core.config import settings


class PDFProcessor:
    """
    Utilities for processing PDF medical reports.

    Supports:
    1. Native text extraction for text-based PDFs.
    2. PDF-to-image conversion for scanned/image-based PDFs.
    """

    @staticmethod
    def extract_native_text(
        pdf_path: str,
    ) -> str:
        """
        Extract text directly from a PDF without OCR.

        This is preferred for text-based PDFs because native
        extraction preserves document text more accurately than OCR.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            Extracted native text. Returns an empty string if
            no usable text is present.
        """

        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"PDF not found: {pdf_path}"
            )

        extracted_pages = []

        with fitz.open(pdf_path) as document:
            for page in document:
                text = page.get_text("text")

                if text and text.strip():
                    extracted_pages.append(
                        text.strip()
                    )

        return "\n\n".join(extracted_pages).strip()

    @staticmethod
    def has_usable_native_text(
        text: str,
        min_characters: int = 50,
    ) -> bool:
        """
        Determine whether native PDF extraction produced
        enough text to avoid OCR.

        A small amount of extracted text can occur in PDFs
        containing only metadata, headers, or other fragments.

        Args:
            text: Native extracted PDF text.
            min_characters: Minimum number of non-whitespace
                characters required.

        Returns:
            True if the extracted text is considered usable.
        """

        if not text:
            return False

        normalized = " ".join(text.split())

        return len(normalized) >= min_characters

    @staticmethod
    def convert_pdf_to_images(
        pdf_path: str,
        dpi: int = 300,
    ) -> list[np.ndarray]:
        """
        Convert every page of a PDF into an OpenCV image.

        This method is used as the OCR fallback when native
        PDF text extraction is unavailable or insufficient.

        Args:
            pdf_path: Path to the PDF file.
            dpi: Resolution used during rendering.

        Returns:
            List of OpenCV images (numpy arrays).
        """

        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"PDF not found: {pdf_path}"
            )

        pages = convert_from_path(
            pdf_path=str(pdf_path),
            dpi=dpi,
            poppler_path=settings.POPPLER_PATH,
        )

        images = []

        for page in pages:
            image = cv2.cvtColor(
                np.array(page),
                cv2.COLOR_RGB2BGR,
            )

            images.append(image)

        return images

