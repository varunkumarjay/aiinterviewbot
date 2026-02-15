class RiskAssessor:

    def __init__(self):
        pass

    def analyze(
        self,
        resume_consistency: dict,
        pattern_analysis: dict,
        skill_depth_data: dict
    ):

        integrity_score = resume_consistency.get("resume_integrity_score", 1)
        bluff_risk = resume_consistency.get("bluff_risk_level", "Low")

        collapse_under_difficulty = pattern_analysis.get("collapse_under_difficulty", False)
        performance_stability = pattern_analysis.get("performance_stability", "Stable")
        average_score = pattern_analysis.get("average_score", 0)

        weakness_clusters = skill_depth_data.get("weakness_clusters", [])

        risk_score = 0

        # Resume integrity impact
        risk_score += (1 - integrity_score) * 0.4

        # Bluff risk impact
        if bluff_risk == "High":
            risk_score += 0.3
        elif bluff_risk == "Moderate":
            risk_score += 0.15

        # Difficulty collapse
        if collapse_under_difficulty:
            risk_score += 0.2

        # Performance instability
        if performance_stability == "Highly Unstable":
            risk_score += 0.15

        # Weak domain clusters
        risk_score += len(weakness_clusters) * 0.05

        risk_score = min(risk_score, 1)

        # Determine risk level
        if risk_score > 0.6:
            risk_level = "High"
        elif risk_score > 0.3:
            risk_level = "Moderate"
        else:
            risk_level = "Low"

        # Hiring confidence calculation
        hiring_confidence = max(0, round((average_score / 5) * (1 - risk_score) * 100, 2))

        return {
            "overall_risk_score": round(risk_score, 2),
            "risk_level": risk_level,
            "hiring_confidence_percent": hiring_confidence
        }
