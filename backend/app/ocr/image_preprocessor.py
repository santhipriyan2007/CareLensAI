import cv2
import numpy as np


class ImagePreprocessor:
    """
    Image preprocessing pipeline for OCR.
    """

    @staticmethod
    def preprocess(
        image: np.ndarray,
    ) -> np.ndarray:
        """
        Prepare an image for OCR.

        Steps:
        1. Convert to grayscale
        2. Reduce noise
        3. Improve contrast
        4. Adaptive threshold
        """

        # Convert to grayscale
        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY,
        )

        # Noise reduction
        denoised = cv2.GaussianBlur(
            gray,
            (5, 5),
            0,
        )

        # Contrast enhancement
        enhanced = cv2.equalizeHist(
            denoised
        )

        # Adaptive threshold
        binary = cv2.adaptiveThreshold(
            enhanced,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11,
            2,
        )

        return binary