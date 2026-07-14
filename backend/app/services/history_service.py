from math import ceil
from uuid import UUID
from datetime import date

from app.repositories.analysis_repository import AnalysisRepository
from app.schemas.history import (
    HistoryItem,
    HistoryResponse,
)


class HistoryService:
    """
    Service responsible for retrieving
    AI analysis history.
    """

    @classmethod
    def get_history(
        cls,
        page: int = 1,
        page_size: int = 10,
        report_id: UUID | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> HistoryResponse:
        """
        Retrieve paginated analysis history.
        """

        result = AnalysisRepository.get_history(
            page=page,
            page_size=page_size,
            report_id=report_id,
            start_date=start_date,
            end_date=end_date,
        )

        history_items: list[HistoryItem] = []

        for record in result["items"]:

            analysis = record.get("analysis", {})

            report = record.get("reports", {})

            history_items.append(
                HistoryItem(
                    analysis_id=record["id"],
                    report_id=record["report_id"],
                    report_name=report.get(
                        "original_file_name",
                        "Unknown Report",
                    ),
                    risk_level=analysis.get(
                        "risk_level",
                        "Unknown",
                    ),
                    urgency=analysis.get(
                        "urgency",
                        "Unknown",
                    ),
                    confidence_score=analysis.get(
                        "confidence_score",
                        0,
                    ),
                    analysis_date=record["created_at"],
                )
            )

        total = result["total"]

        total_pages = ceil(total / page_size) if total else 0

        return HistoryResponse(
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
            items=history_items,
        )