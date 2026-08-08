from typing import Literal
from uuid import UUID

from pydantic import BaseModel

from app.schemas.analysis import AIAnalysis, AbnormalFinding


ComparisonStatus = Literal[
    "improved",
    "worsened",
    "stable",
]


OverallTrend = Literal[
    "Improved",
    "Worsened",
    "Stable",
    "Mixed",
]


class ChangeResult(BaseModel):
    """
    Represents the deterministic change between
    a previous and current categorical value.
    """

    previous: str
    current: str
    change: ComparisonStatus


class ConfidenceChange(BaseModel):
    """
    Represents the change in AI confidence score.

    This is analysis metadata and does not represent
    clinical improvement or deterioration.
    """

    previous: int
    current: int
    difference: int


class AbnormalityComparison(BaseModel):
    """
    Represents changes in abnormal findings between
    two medical report analyses.
    """

    new: list[AbnormalFinding]
    resolved: list[AbnormalFinding]
    persistent: list[AbnormalFinding]


class CompareReportsResponse(BaseModel):
    """
    Response returned by the Compare Reports API.

    Contains the original validated AI analyses along
    with deterministic comparison results.
    """

    previous_report_id: UUID
    current_report_id: UUID

    previous_analysis: AIAnalysis
    current_analysis: AIAnalysis

    risk_change: ChangeResult
    urgency_change: ChangeResult
    confidence_change: ConfidenceChange

    abnormality_comparison: AbnormalityComparison

    overall_trend: OverallTrend