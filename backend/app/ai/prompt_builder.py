"""
Prompt Builder

Responsibilities:
- Build prompts dynamically
- Inject OCR text into prompt templates
- Support future prompt variations
"""

from app.ai.medical_prompts import MEDICAL_REPORT_ANALYSIS_PROMPT


class PromptBuilder:
    """
    Builds prompts for AI analysis.
    """

    @staticmethod
    def build_medical_report_prompt(report_text: str) -> str:
        """
        Build the medical report analysis prompt.

        Args:
            report_text: OCR extracted medical report text.

        Returns:
            Complete prompt ready to be sent to Gemini.
        """

        return MEDICAL_REPORT_ANALYSIS_PROMPT.format(
            report_text=report_text
        )