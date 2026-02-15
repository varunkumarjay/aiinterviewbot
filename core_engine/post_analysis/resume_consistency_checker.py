class ResumeConsistencyChecker:

    def __init__(self):
        pass

    def analyze(
        self,
        role_profile: dict,
        alignment_data: dict,
        metadata: dict
    ):
        """
        Compare resume claims with demonstrated performance.
        """

        claimed_skills = alignment_data.get("claimed_skills", [])
        domain_strength = metadata.get("domain_strength", {})
        bluff_trend = metadata.get("bluff_trend", [])

        overclaim_flags = []
        underperformance_flags = []

        # 1️⃣ Check if claimed skills show low depth
        for skill in claimed_skills:
            avg_depth = domain_strength.get(skill, None)

            if avg_depth is not None and avg_depth < 2.5:
                overclaim_flags.append(
                    f"Claimed strong skill in '{skill}' but demonstrated shallow depth."
                )

        # 2️⃣ Check bluff trend consistency
        avg_bluff = sum(bluff_trend) / len(bluff_trend) if bluff_trend else 0

        bluff_risk = "Low"
        if avg_bluff > 0.6:
            bluff_risk = "High"
        elif avg_bluff > 0.3:
            bluff_risk = "Moderate"

        # 3️⃣ Compute resume integrity score
        penalty = len(overclaim_flags) * 0.15 + avg_bluff * 0.3
        integrity_score = max(0, round(1 - penalty, 2))

        return {
            "resume_integrity_score": integrity_score,
            "bluff_risk_level": bluff_risk,
            "overclaim_flags": overclaim_flags,
            "underperformance_flags": underperformance_flags
        }
