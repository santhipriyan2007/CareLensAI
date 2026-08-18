"""
Prompt Builder

Responsibilities:

- Build prompts dynamically
- Inject OCR text into prompt templates
- Build grounded RAG prompts
- Perform lightweight prompt preprocessing
- Support future prompt variations
"""

from app.ai.medical_prompts import MEDICAL_REPORT_ANALYSIS_PROMPT


class PromptBuilder:
    """
    Builds prompts for AI analysis and RAG-based responses.
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
    def build_medical_report_prompt(
        cls,
        report_text: str,
    ) -> str:
        """
        Build the medical report analysis prompt.

        Args:
            report_text: OCR extracted medical report text.

        Returns:
            Complete prompt ready to be sent to Gemini.
        """

        cleaned_text = cls._clean_report_text(
            report_text
        )

        return MEDICAL_REPORT_ANALYSIS_PROMPT.format(
            report_text=cleaned_text
        )

    @classmethod
    def build_rag_prompt(
        cls,
        question: str,
        context: str,
    ) -> str:
        """
        Build a grounded prompt using retrieved report context.

        The model is explicitly instructed to use the supplied
        context as the source of information and avoid inventing
        information that is not present in the retrieved context.

        Args:
            question: User's question about the medical report.
            context: Relevant context retrieved from the report.

        Returns:
            Complete grounded prompt ready for Gemini.
        """

        cleaned_question = question.strip()
        cleaned_context = cls._clean_report_text(context)

        if not cleaned_question:
            raise ValueError(
                "Question cannot be empty."
            )

        if not cleaned_context:
            raise ValueError(
                "Retrieved context cannot be empty."
            )

        return f"""
You are an AI assistant supporting a clinical decision-support
application called CareLens AI.

Your task is to answer the user's question using ONLY the
retrieved medical report context provided below.

IMPORTANT RULES:

1. Use the retrieved context as the primary source of information.
2. Do not invent medical values, symptoms, diagnoses, or facts.
3. Do not assume information that is not present in the context.
4. If the context does not contain enough information to answer
   the question, clearly say that the available report context
   does not provide enough information.
5. Preserve uncertainty when the report or OCR text is uncertain.
6. Distinguish reported findings from medical interpretation.
7. Do not provide a definitive medical diagnosis.
8. Do not claim that a finding proves a particular disease.
9. Keep the response clear and understandable.
10. If the question involves medical interpretation or clinical
    action, briefly state that the finding should be reviewed by a
    qualified healthcare professional, but do not add a separate
    disclaimer or generic closing statement.
11. Do not include a medical disclaimer in your response.
12. Do not write "Medical disclaimer:".
13. Do not repeat or generate any disclaimer text.
14. The application will provide the official medical disclaimer
    separately.
15. If the retrieved context contains conflicting, incomplete, or
    OCR-corrupted reference ranges for the same test, do not choose
    one arbitrarily.
16. If a reference range is unclear or conflicting, explicitly state
    that the report context is unclear rather than declaring the
    value normal or abnormal.
17. Do not override the report's stated reference range using general
    medical knowledge unless the user specifically asks for general
    medical information.
18. When interpreting a test result, distinguish clearly between:
    - the reported value,
    - the report's reference range,
    - and any medical interpretation.

RETRIEVED MEDICAL REPORT CONTEXT:

{cleaned_context}

USER QUESTION:

{cleaned_question}

Provide a concise, evidence-grounded response based only on the
retrieved context.

Return ONLY the answer to the user's question.
Do not add a medical disclaimer.
""".strip()