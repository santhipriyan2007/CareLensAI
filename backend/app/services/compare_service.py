from uuid import UUID

from fastapi import HTTPException, status

from app.repositories.analysis_repository import AnalysisRepository
from app.schemas.analysis import AIAnalysis
from app.schemas.compare import CompareReportsResponse
from app.services.comparison_engine import ComparisonEngine


class CompareService:
    """
    Service responsible for orchestrating
    report comparison workflows.
    """

    @classmethod
    def get_reports_for_comparison(
        cls,
        previous_report_id: UUID,
        current_report_id: UUID,
    ) -> CompareReportsResponse:
        """
        Retrieve and compare AI analyses for two reports.
        """

        previous_analysis, current_analysis = (
            AnalysisRepository.get_compare_reports(
                previous_report_id,
                current_report_id,
            )
        )

        if previous_analysis is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Previous report analysis not found.",
            )

        if current_analysis is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Current report analysis not found.",
            )

        previous_ai_analysis = AIAnalysis.model_validate(
            previous_analysis["analysis"]
        )

        current_ai_analysis = AIAnalysis.model_validate(
            current_analysis["analysis"]
        )

        comparison = ComparisonEngine.compare(
            previous=previous_ai_analysis,
            current=current_ai_analysis,
        )

        return CompareReportsResponse(
            previous_report_id=previous_report_id,
            current_report_id=current_report_id,
            previous_analysis=previous_ai_analysis,
            current_analysis=current_ai_analysis,
            **comparison,
        )