class HiringRecommendationEngine:

    def __init__(self):
        pass

    def generate(
        self,
        risk_data: dict,
        resume_consistency: dict,
        pattern_analysis: dict,
        skill_depth_data: dict
    ):

        hiring_confidence = risk_data.get("hiring_confidence_percent", 0)
        risk_level = risk_data.get("risk_level", "High")

        strength_clusters = skill_depth_data.get("strength_clusters", [])
        weakness_clusters = skill_depth_data.get("weakness_clusters", [])

        performance_trajectory = pattern_analysis.get("performance_trajectory", "Flat")

        recommendation = "Reject"
        rationale = []

        # Core recommendation logic
        if hiring_confidence >= 75 and risk_level == "Low":
            recommendation = "Strong Hire"
        elif hiring_confidence >= 60 and risk_level in ["Low", "Moderate"]:
            recommendation = "Hire"
        elif hiring_confidence >= 45:
            recommendation = "Hire with Caution"
        else:
            recommendation = "Reject"

        # Build rationale
        if strength_clusters:
            rationale.append(f"Demonstrated strong depth in: {', '.join(strength_clusters)}.")

        if weakness_clusters:
            rationale.append(f"Weakness observed in: {', '.join(weakness_clusters)}.")

        if performance_trajectory == "Improving":
            rationale.append("Performance improved as difficulty increased.")
        elif performance_trajectory == "Declining":
            rationale.append("Performance declined under progressive difficulty.")

        if risk_level == "High":
            rationale.append("High overall risk detected from behavioral and integrity signals.")

        return {
            "final_recommendation": recommendation,
            "hiring_confidence_percent": hiring_confidence,
            "risk_level": risk_level,
            "executive_rationale": " ".join(rationale)
        }
