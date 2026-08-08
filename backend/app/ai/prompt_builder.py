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
10. Encourage consultation with a qualified healthcare professional
    when medical interpretation or clinical action is involved.

RETRIEVED MEDICAL REPORT CONTEXT:

{cleaned_context}

USER QUESTION:

{cleaned_question}

Provide a concise, evidence-grounded response based only on the
retrieved context.

Medical disclaimer:
This response is AI-generated for clinical decision support and
does not replace evaluation or advice from a qualified healthcare
professional.
""".strip()