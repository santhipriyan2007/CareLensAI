import cv2
import numpy as np
import pytesseract

from app.core.config import settings


class TesseractEngine:
    """
    Wrapper around Tesseract OCR.
    """

    @staticmethod
    def extract_text(
        image: np.ndarray,
    ) -> str:
        """
        Extract text using Tesseract OCR.
        """

        pytesseract.pytesseract.tesseract_cmd = (
            settings.TESSERACT_CMD
        )

        rgb_image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB,
        )

        text = pytesseract.image_to_string(
            rgb_image,
            lang="eng",
        )

        return text.strip()