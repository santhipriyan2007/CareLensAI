import re


class TextCleaner:
    """
    Cleans OCR output before AI processing.
    """

    @staticmethod
    def clean(
        text: str,
    ) -> str:
        """
        Normalize OCR text.
        """

        if not text:
            return ""

        # Normalize line endings
        text = text.replace("\r", "\n")

        # Remove tabs
        text = text.replace("\t", " ")

        # Remove multiple spaces
        text = re.sub(
            r"[ ]{2,}",
            " ",
            text,
        )

        # Remove excessive blank lines
        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text,
        )

        # Remove spaces before punctuation
        text = re.sub(
            r"\s+([.,:%)])",
            r"\1",
            text,
        )

        # Remove spaces after opening brackets
        text = re.sub(
            r"([(\[])\s+",
            r"\1",
            text,
        )

        return text.strip()