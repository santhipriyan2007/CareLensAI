from pathlib import Path

import cv2
import numpy as np
import fitz
from pdf2image import convert_from_path

from app.core.config import settings


class PDFProcessor:

    @staticmethod
    def extract_native_text(pdf_path: str) -> str:
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

        return "\n\n".join(
            extracted_pages
        ).strip()

    @staticmethod
    def has_usable_native_text(
        text: str,
        min_characters: int = 50,
    ) -> bool:
        if not text:
            return False

        normalized = " ".join(
            text.split()
        )

        return len(normalized) >= min_characters

    @staticmethod
    def convert_pdf_to_images(
        pdf_path: str,
        dpi: int = 300,
    ) -> list[np.ndarray]:

        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(
                f"PDF not found: {pdf_path}"
            )

        pages = convert_from_path(
            pdf_path=str(pdf_path),
            dpi=dpi,
            poppler_path=(
                settings.POPPLER_PATH
                if settings.POPPLER_PATH
                else None
            ),
        )

        images = []

        for page in pages:
            image = cv2.cvtColor(
                np.array(page),
                cv2.COLOR_RGB2BGR,
            )

            images.append(image)

        return images

