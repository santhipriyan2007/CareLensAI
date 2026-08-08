from app.schemas.analysis import AIAnalysis, AbnormalFinding
from app.schemas.compare import (
    AbnormalityComparison,
    ChangeResult,
    ConfidenceChange,
    OverallTrend,
)


class ComparisonEngine:
    """
    Deterministic comparison engine for two AI analyses.

    This class performs factual comparisons using
    application logic rather than generative AI.
    """

    RISK_LEVEL_ORDER = {
        "Low": 1,
        "Moderate": 2,
        "High": 3,
        "Critical": 4,
    }

    URGENCY_ORDER = {
        "Routine": 1,
        "Soon": 2,
        "Urgent": 3,
        "Emergency": 4,
    }

    @classmethod
    def compare(
        cls,
        previous: AIAnalysis,
        current: AIAnalysis,
    ) -> dict:
        """
        Compare two validated AI analyses.
        """

        risk_change = cls._compare_ordered_value(
            previous=previous.risk_level,
            current=current.risk_level,
            order=cls.RISK_LEVEL_ORDER,
        )

        urgency_change = cls._compare_ordered_value(
            previous=previous.urgency,
            current=current.urgency,
            order=cls.URGENCY_ORDER,
        )

        confidence_change = cls._compare_confidence(
            previous.confidence_score,
            current.confidence_score,
        )

        abnormality_comparison = cls._compare_abnormalities(
            previous.abnormal_findings,
            current.abnormal_findings,
        )

        overall_trend = cls._determine_overall_trend(
            risk_change=risk_change.change,
            urgency_change=urgency_change.change,
            abnormality_comparison=abnormality_comparison,
        )

        return {
            "risk_change": risk_change,
            "urgency_change": urgency_change,
            "confidence_change": confidence_change,
            "abnormality_comparison": abnormality_comparison,
            "overall_trend": overall_trend,
        }

    @classmethod
    def _compare_ordered_value(
        cls,
        previous: str,
        current: str,
        order: dict[str, int],
    ) -> ChangeResult:
        """
        Compare categorical values using an explicit severity order.
        """

        previous_value = order[previous]
        current_value = order[current]

        if current_value < previous_value:
            change = "improved"
        elif current_value > previous_value:
            change = "worsened"
        else:
            change = "stable"

        return ChangeResult(
            previous=previous,
            current=current,
            change=change,
        )

    @classmethod
    def _compare_confidence(
        cls,
        previous: int,
        current: int,
    ) -> ConfidenceChange:
        """
        Calculate the difference between two AI confidence scores.
        """

        return ConfidenceChange(
            previous=previous,
            current=current,
            difference=current - previous,
        )

    @classmethod
    def _compare_abnormalities(
        cls,
        previous: list[AbnormalFinding],
        current: list[AbnormalFinding],
    ) -> AbnormalityComparison:
        """
        Compare abnormal findings using normalized parameters.
        """

        previous_map = cls._build_abnormality_map(previous)
        current_map = cls._build_abnormality_map(current)

        previous_parameters = set(previous_map.keys())
        current_parameters = set(current_map.keys())

        persistent_parameters = (
            previous_parameters & current_parameters
        )

        resolved_parameters = (
            previous_parameters - current_parameters
        )

        new_parameters = (
            current_parameters - previous_parameters
        )

        persistent = [
            current_map[parameter]
            for parameter in sorted(persistent_parameters)
        ]

        resolved = [
            previous_map[parameter]
            for parameter in sorted(resolved_parameters)
        ]

        new = [
            current_map[parameter]
            for parameter in sorted(new_parameters)
        ]

        return AbnormalityComparison(
            new=new,
            resolved=resolved,
            persistent=persistent,
        )

    @classmethod
    def _build_abnormality_map(
        cls,
        findings: list[AbnormalFinding],
    ) -> dict[str, AbnormalFinding]:
        """
        Build a normalized parameter-to-finding mapping.
        """

        result: dict[str, AbnormalFinding] = {}

        for finding in findings:
            parameter = finding.parameter.strip().lower()

            if not parameter:
                continue

            result[parameter] = finding

        return result

    @classmethod
    def _determine_overall_trend(
        cls,
        risk_change: str,
        urgency_change: str,
        abnormality_comparison: AbnormalityComparison,
    ) -> OverallTrend:
        """
        Determine the overall deterministic trend.

        Risk and urgency are given higher importance than
        abnormality counts.
        """

        signals: list[str] = [
            risk_change,
            urgency_change,
        ]

        if abnormality_comparison.new and not abnormality_comparison.resolved:
            signals.append("worsened")

        elif abnormality_comparison.resolved and not abnormality_comparison.new:
            signals.append("improved")

        elif (
            abnormality_comparison.new
            and abnormality_comparison.resolved
        ):
            signals.append("mixed")

        else:
            signals.append("stable")

        if "mixed" in signals:
            return "Mixed"

        improved_count = signals.count("improved")
        worsened_count = signals.count("worsened")
        stable_count = signals.count("stable")

        if improved_count > 0 and worsened_count > 0:
            return "Mixed"

        if improved_count > worsened_count:
            return "Improved"

        if worsened_count > improved_count:
            return "Worsened"

        if stable_count == len(signals):
            return "Stable"

        return "Mixed"