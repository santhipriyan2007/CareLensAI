from pathlib import Path

import cv2
import numpy as np
from pdf2image import convert_from_path

from app.core.config import settings


class PDFProcessor:
    """
    Converts PDF files into OpenCV images.
    """

    @staticmethod
    def convert_pdf_to_images(
        pdf_path: str,
        dpi: int = 300,
    ) -> list[np.ndarray]:
        """
        Convert every page of a PDF into an OpenCV image.

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