from app.database.supabase import supabase


class AnalyticsRepository:
    """
    Repository responsible for database operations
    required by the analytics module.
    """

    REPORTS_TABLE = "reports"
    ANALYSES_TABLE = "analyses"

    @classmethod
    def get_overview_data(cls) -> dict:
        """
        Retrieve raw data required for analytics overview metrics.

        Returns:
            Dictionary containing:
            - total_reports
            - total_analyses
            - total_patients
            - abnormal_reports
        """

        # Total reports
        reports_response = (
            supabase.table(cls.REPORTS_TABLE)
            .select("id", count="exact")
            .execute()
        )

        total_reports = reports_response.count or 0

        # Unique patients
        patients_response = (
            supabase.table(cls.REPORTS_TABLE)
            .select("patient_user_id")
            .execute()
        )

        patient_ids = {
            record["patient_user_id"]
            for record in (patients_response.data or [])
            if record.get("patient_user_id")
        }

        total_patients = len(patient_ids)

        # Total analyses and abnormal reports
        analyses_response = (
            supabase.table(cls.ANALYSES_TABLE)
            .select("id, analysis", count="exact")
            .execute()
        )

        analyses = analyses_response.data or []

        total_analyses = analyses_response.count or 0

        abnormal_reports = 0

        for record in analyses:
            analysis = record.get("analysis") or {}

            abnormal_findings = analysis.get(
                "abnormal_findings",
                [],
            )

            if (
                isinstance(abnormal_findings, list)
                and abnormal_findings
            ):
                abnormal_reports += 1

        return {
            "total_reports": total_reports,
            "total_analyses": total_analyses,
            "total_patients": total_patients,
            "abnormal_reports": abnormal_reports,
        }

    @classmethod
    def get_risk_distribution(cls) -> dict[str, int]:
        """
        Retrieve the number of analyses for each
        valid risk level.

        Analyses created using older schemas that do
        not contain a valid risk_level are excluded
        from the risk distribution.
        """

        response = (
            supabase.table(cls.ANALYSES_TABLE)
            .select("analysis")
            .execute()
        )

        distribution = {
            "Low": 0,
            "Moderate": 0,
            "High": 0,
            "Critical": 0,
        }

        valid_risk_levels = {
            "Low",
            "Moderate",
            "High",
            "Critical",
        }

        for record in response.data or []:
            analysis = record.get("analysis") or {}

            risk_level = analysis.get("risk_level")

            if risk_level in valid_risk_levels:
                distribution[risk_level] += 1

        return distribution

    @classmethod
    def get_report_trends(cls) -> list[dict]:
        """
        Retrieve report upload dates for trend analysis.

        The service layer is responsible for converting
        these dates into the final API response format.
        """

        response = (
            supabase.table(cls.REPORTS_TABLE)
            .select("uploaded_at")
            .order("uploaded_at", desc=False)
            .execute()
        )

        return response.data or []