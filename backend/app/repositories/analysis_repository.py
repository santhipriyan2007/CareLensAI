from datetime import date
from uuid import UUID

from app.database.supabase import supabase


class AnalysisRepository:
    """
    Repository responsible for all database
    operations related to AI analyses.
    """

    TABLE_NAME = "analyses"

    @classmethod
    def save_analysis(
        cls,
        report_id: UUID,
        ocr_text: str,
        analysis: dict,
    ) -> dict:
        """
        Save a completed AI analysis.
        """

        response = (
            supabase.table(cls.TABLE_NAME)
            .insert(
                {
                    "report_id": str(report_id),
                    "ocr_text": ocr_text,
                    "analysis": analysis,
                }
            )
            .execute()
        )

        return response.data[0]

    @classmethod
    def get_by_report_id(
        cls,
        report_id: UUID,
    ):
        """
        Retrieve an analysis using report ID.
        """

        response = (
            supabase.table(cls.TABLE_NAME)
            .select("*")
            .eq("report_id", str(report_id))
            .execute()
        )

        if not response.data:
            return None

        return response.data[0]

    @classmethod
    def get_compare_reports(
        cls,
        previous_report_id: UUID,
        current_report_id: UUID,
    ) -> tuple[dict | None, dict | None]:
        """
        Retrieve analyses for two reports.

        Returns:
            (
                previous_report_analysis,
                current_report_analysis,
            )
        """

        previous_analysis = cls.get_by_report_id(previous_report_id)
        current_analysis = cls.get_by_report_id(current_report_id)

        return previous_analysis, current_analysis

    @classmethod
    def get_history(
        cls,
        page: int = 1,
        page_size: int = 10,
        report_id: UUID | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> dict:
        """
        Retrieve paginated analysis history.

        Supports:
        - Pagination
        - Report filtering
        - Analysis date filtering
        """

        query = (
            supabase.table(cls.TABLE_NAME)
            .select(
                """
                *,
                reports(
                    id,
                    patient_user_id,
                    original_file_name,
                    uploaded_at
                )
                """,
                count="exact",
            )
            .order("created_at", desc=True)
        )

        # Filter by report
        if report_id:
            query = query.eq("report_id", str(report_id))

        # Filter by analysis date
        if start_date:
            query = query.gte(
                "created_at",
                start_date.isoformat(),
            )

        if end_date:
            query = query.lte(
                "created_at",
                end_date.isoformat(),
            )

        # Pagination
        start = (page - 1) * page_size
        end = start + page_size - 1

        response = query.range(start, end).execute()

        return {
            "items": response.data or [],
            "total": response.count or 0,
        }

   