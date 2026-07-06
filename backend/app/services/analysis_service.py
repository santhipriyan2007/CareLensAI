"""
Analysis Service

Responsibilities:
- Orchestrate AI analysis workflow
- Build prompts
- Call Gemini
- Validate JSON responses
"""

from app.ai.gemini_client import GeminiClient
from app.ai.json_validator import JSONValidator
from app.ai.prompt_builder import PromptBuilder


class AnalysisService:
    """
    Handles AI-powered medical report analysis.
    """

    def __init__(self):
        self.gemini = GeminiClient()

    def analyze_text(self, report_text: str) -> dict:
        """
        Analyze OCR extracted medical report text.

        Args:
            report_text: OCR extracted report text.

        Returns:
            Structured AI analysis dictionary.
        """

        prompt = PromptBuilder.build_medical_report_prompt(
            report_text
        )

        ai_response = self.gemini.generate(prompt)

        analysis = JSONValidator.parse(ai_response)

        return analysis