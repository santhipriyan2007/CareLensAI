from fastapi import APIRouter, Depends

from app.core.dependencies import require_role
from app.schemas.analytics import (
    AnalyticsOverview,
    AnalyticsTrendResponse,
    RiskDistributionResponse,
)
from app.services.analytics_service import AnalyticsService


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get(
    "/overview",
    response_model=AnalyticsOverview,
)
def get_analytics_overview(
    current_user=Depends(require_role("doctor")),
):
    """
    Retrieve high-level analytics metrics.
    """

    return AnalyticsService.get_overview()


@router.get(
    "/risk-distribution",
    response_model=RiskDistributionResponse,
)
def get_risk_distribution(
    current_user=Depends(require_role("doctor")),
):
    """
    Retrieve analysis risk-level distribution.
    """

    return AnalyticsService.get_risk_distribution()


@router.get(
    "/trends",
    response_model=AnalyticsTrendResponse,
)
def get_report_trends(
    current_user=Depends(require_role("doctor")),
):
    """
    Retrieve report upload trends grouped by month.
    """

    return AnalyticsService.get_report_trends()