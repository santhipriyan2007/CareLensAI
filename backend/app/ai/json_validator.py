"""
JSON Validator

Responsibilities:
- Parse Gemini responses
- Validate JSON format
- Remove markdown wrappers
"""

import json


class JSONValidator:
    """
    Validates and parses AI JSON responses.
    """

    @staticmethod
    def parse(response_text: str) -> dict:
        """
        Parse AI response into a Python dictionary.

        Args:
            response_text: Raw text returned by Gemini.

        Returns:
            Parsed dictionary.

        Raises:
            ValueError: If the response is not valid JSON.
        """

        cleaned = response_text.strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned.replace("```json", "", 1)

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        cleaned = cleaned.strip()

        try:
            return json.loads(cleaned)

        except json.JSONDecodeError as e:
            raise ValueError(
                "Gemini returned invalid JSON."
            ) from e