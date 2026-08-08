from datetime import datetime

from app.repositories.analytics_repository import AnalyticsRepository
from app.schemas.analytics import (
    AnalyticsOverview,
    AnalyticsTrendResponse,
    RiskDistributionItem,
    RiskDistributionResponse,
    TrendItem,
)


class AnalyticsService:
    """
    Service responsible for analytics business logic
    and transformation of repository data into
    API response schemas.
    """

    @classmethod
    def get_overview(cls) -> AnalyticsOverview:
        """
        Retrieve analytics overview metrics.
        """

        data = AnalyticsRepository.get_overview_data()

        return AnalyticsOverview(
            total_reports=data["total_reports"],
            total_analyses=data["total_analyses"],
            total_patients=data["total_patients"],
            abnormal_reports=data["abnormal_reports"],
        )

    @classmethod
    def get_risk_distribution(
        cls,
    ) -> RiskDistributionResponse:
        """
        Retrieve and format analysis risk distribution.
        """

        distribution = AnalyticsRepository.get_risk_distribution()

        items = [
            RiskDistributionItem(
                risk_level=risk_level,
                count=count,
            )
            for risk_level, count in distribution.items()
        ]

        return RiskDistributionResponse(
            distribution=items,
        )

    @classmethod
    def get_report_trends(
        cls,
    ) -> AnalyticsTrendResponse:
        """
        Retrieve report upload timestamps and aggregate
        them by month.
        """

        records = AnalyticsRepository.get_report_trends()

        monthly_counts: dict[str, int] = {}

        for record in records:
            uploaded_at = record.get("uploaded_at")

            if not uploaded_at:
                continue

            try:
                timestamp = datetime.fromisoformat(
                    uploaded_at.replace("Z", "+00:00")
                )
            except (ValueError, TypeError):
                continue

            period = timestamp.strftime("%Y-%m")

            monthly_counts[period] = (
                monthly_counts.get(period, 0) + 1
            )

        trends = [
            TrendItem(
                period=period,
                count=count,
            )
            for period, count in sorted(
                monthly_counts.items()
            )
        ]

        return AnalyticsTrendResponse(
            trends=trends,
        )