from uuid import UUID

from fastapi import HTTPException, status

from app.ai.gemini_client import GeminiClient
from app.ai.prompt_builder import PromptBuilder
from app.repositories.analysis_repository import AnalysisRepository
from app.rag.rag_service import RAGService
from app.schemas.chat import ChatResponse
from app.schemas.user import UserResponse
from app.services.report_service import ReportService


class ChatService:
    """
    Service responsible for report-aware AI medical chat.
    """

    MEDICAL_DISCLAIMER = (
        "This response is AI-generated for clinical decision support "
        "and does not replace evaluation or advice from a qualified "
        "healthcare professional."
    )

    @staticmethod
    async def chat(
        report_id: UUID,
        question: str,
        current_user: UserResponse,
    ) -> ChatResponse:
        """
        Generate a grounded AI response using a medical report
        as the retrieval source.
        """

        cleaned_question = question.strip()

        if not cleaned_question:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Question cannot be empty.",
            )

        # Step 1: Verify that the user can access the report.
        ReportService._get_authorized_report(
            report_id=report_id,
            current_user=current_user,
        )

        # Step 2: Retrieve the existing analysis/OCR record.
        analysis = AnalysisRepository.get_by_report_id(
            report_id
        )

        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No analysis found for this report.",
            )

        ocr_text = analysis.get("ocr_text")

        if not ocr_text or not ocr_text.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="No OCR text is available for this report.",
            )

        # Step 3: Build a temporary report-specific RAG index.
        rag_service = RAGService()

        rag_service.index_document(
            ocr_text
        )

        # Step 4: Retrieve context relevant to the user's question.
        context = rag_service.retrieve_context(
            query=cleaned_question,
            top_k=3,
        )

        if not context or not context.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=(
                    "No relevant information was found in the "
                    "medical report for this question."
                ),
            )

        # Step 5: Build a grounded medical prompt.
        prompt = PromptBuilder.build_rag_prompt(
            question=cleaned_question,
            context=context,
        )

        # Step 6: Generate the response with Gemini.
        client = GeminiClient()

        answer = client.generate(prompt)

        if not answer or not answer.strip():
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="AI service returned an empty response.",
            )

        return ChatResponse(
            report_id=report_id,
            question=cleaned_question,
            answer=answer.strip(),
            medical_disclaimer=ChatService.MEDICAL_DISCLAIMER,
        )