"""
Prompt Builder

Responsibilities:
- Build prompts dynamically
- Inject OCR text into prompt templates
- Perform lightweight prompt preprocessing
- Support future prompt variations
"""

from app.ai.medical_prompts import MEDICAL_REPORT_ANALYSIS_PROMPT


class PromptBuilder:
    """
    Builds prompts for AI analysis.
    """

    @staticmethod
    def _clean_report_text(report_text: str) -> str:
        """
        Perform lightweight cleanup on OCR text before
        sending it to the AI model.

        Args:
            report_text: Raw OCR extracted text.

        Returns:
            Cleaned report text.
        """

        return "\n".join(
            line.strip()
            for line in report_text.splitlines()
            if line.strip()
        )

    @classmethod
    def build_medical_report_prompt(cls, report_text: str) -> str:
        """
        Build the medical report analysis prompt.

        Args:
            report_text: OCR extracted medical report text.

        Returns:
            Complete prompt ready to be sent to Gemini.
        """

        cleaned_text = cls._clean_report_text(report_text)

        return MEDICAL_REPORT_ANALYSIS_PROMPT.format(
            report_text=cleaned_text
        )