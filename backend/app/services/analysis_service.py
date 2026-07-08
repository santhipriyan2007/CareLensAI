"""
Analysis Service

Responsibilities:
- Analyze OCR text using Gemini
- Persist AI analysis
- Orchestrate complete AI workflow
"""

import os
from datetime import datetime
from uuid import UUID

from app.ai.gemini_client import GeminiClient
from app.ai.json_validator import JSONValidator
from app.ai.prompt_builder import PromptBuilder
from app.repositories.analysis_repository import AnalysisRepository
from app.schemas.analysis import (
    AIAnalysis,
    AnalysisCreateResponse,
    AnalysisResponse,
)
from app.services.ocr_service import OCRService
from app.services.report_service import ReportService
from app.storage.storage_service import StorageService


class AnalysisService:
    """
    Coordinates the complete AI analysis workflow.
    """

    def __init__(
        self,
        gemini_client: GeminiClient | None = None,
    ):
        self.gemini = gemini_client or GeminiClient()

    @staticmethod
    def _to_response(data: dict) -> AnalysisResponse:
        """
        Convert repository dictionary into
        API response schema.
        """

        return AnalysisResponse(
            id=data["id"],
            report_id=data["report_id"],
            analysis=AIAnalysis.model_validate(
                data["analysis"]
            ),
            created_at=datetime.fromisoformat(
                data["created_at"].replace("Z", "+00:00")
            ),
        )

    def analyze_text(
        self,
        report_text: str,
    ) -> AIAnalysis:
        """
        Analyze OCR extracted report text.

        Args:
            report_text: OCR extracted medical report text.

        Returns:
            Validated AIAnalysis object.
        """

        prompt = PromptBuilder.build_medical_report_prompt(
            report_text
        )

        ai_response = self.gemini.generate(prompt)

        validated = JSONValidator.parse(
            ai_response
        )

        return AIAnalysis.model_validate(
            validated
        )

    def save_analysis(
        self,
        report_id: UUID,
        ocr_text: str,
        analysis: AIAnalysis,
    ) -> AnalysisResponse:
        """
        Persist AI analysis.

        Args:
            report_id: Report ID.
            ocr_text: OCR extracted text.
            analysis: Validated AI analysis.

        Returns:
            Saved analysis response.
        """

        saved = AnalysisRepository.save_analysis(
            report_id=report_id,
            ocr_text=ocr_text,
            analysis=analysis.model_dump(),
        )

        return self._to_response(
            saved
        )

    def analyze_report(
        self,
        report_id: UUID,
    ) -> AnalysisCreateResponse:
        """
        Perform the complete AI analysis workflow for a report.
        """

        # Return existing analysis if already available
        existing = AnalysisRepository.get_by_report_id(
            report_id
        )

        if existing:
            return AnalysisCreateResponse(
                message="Analysis already exists.",
                analysis=self._to_response(
                    existing
                ),
            )

        # Fetch report metadata
        report = ReportService.get_report_record(
            report_id
        )

        # Download report from storage
        pdf_path = StorageService.download_to_temp_file(
            report["storage_path"]
        )

        try:
            # OCR Extraction
            ocr_text = OCRService.extract_text_from_pdf(
                pdf_path
            )

            # AI Analysis
            analysis = self.analyze_text(
                ocr_text
            )

            # Save Analysis
            saved_analysis = self.save_analysis(
                report_id=report_id,
                ocr_text=ocr_text,
                analysis=analysis,
            )

            return AnalysisCreateResponse(
                message="Analysis completed successfully.",
                analysis=saved_analysis,
            )

        finally:
            # Always clean up temporary file
            if os.path.exists(
                pdf_path
            ):
                os.remove(
                    pdf_path
                )