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

   