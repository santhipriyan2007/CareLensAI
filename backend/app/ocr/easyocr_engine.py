import easyocr
import numpy as np


class EasyOCREngine:
    """
    Wrapper around EasyOCR.
    """

    _reader = None

    @classmethod
    def get_reader(cls):
        """
        Lazily initialize the EasyOCR reader.
        """

        if cls._reader is None:
            cls._reader = easyocr.Reader(
                ["en"],
                gpu=False,
            )

        return cls._reader

    @classmethod
    def extract_text(
        cls,
        image: np.ndarray,
    ) -> str:
        """
        Extract text from an OpenCV image.
        """

        reader = cls.get_reader()

        results = reader.readtext(
            image,
            detail=0,
            paragraph=True,
        )

        return "\n".join(results)