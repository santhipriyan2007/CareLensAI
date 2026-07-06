"""
Gemini Client

Responsibilities:
- Initialize Gemini SDK
- Authenticate using API key
- Generate AI responses
- Handle API errors
"""

import logging

from google import genai

from app.core.config import settings

logger = logging.getLogger(__name__)


class GeminiClient:
    """
    Handles communication with Google Gemini.
    """

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model_name = settings.GEMINI_MODEL

    def generate(self, prompt: str) -> str:
        """
        Generate a response from Gemini.

        Args:
            prompt: Complete prompt text.

        Returns:
            AI generated response as plain text.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )

            return response.text

        except Exception as e:
            logger.exception("Gemini API request failed.")

            raise RuntimeError(
                f"Failed to generate AI response: {e}"
            ) from e