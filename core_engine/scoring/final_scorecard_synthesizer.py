class FinalScorecardSynthesizer:

    def __init__(self):
        pass

    def synthesize(
        self,
        pattern_analysis,
        resume_consistency,
        risk_data,
        deep_reasoning_data
    ):

        composite_score = (
            pattern_analysis.get("average_score", 0) * 0.4 +
            resume_consistency.get("resume_integrity_score", 0) * 5 * 0.2 +
            deep_reasoning_data.get("logical_consistency_score", 0) * 0.2 +
            (1 - risk_data.get("overall_risk_score", 0)) * 5 * 0.2
        )

        return {
            "composite_score": round(composite_score, 2)
        }
