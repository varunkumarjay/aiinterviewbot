from datetime import datetime


class AdminReportGenerator:

    def generate(
        self,
        final_evaluation: dict,
        transcript_data: dict,
        role_profile: dict,
        alignment_data: dict
    ):

        criterion_scores = final_evaluation.get("criterion_scores", {})
        strengths = final_evaluation.get("strengths", [])
        weaknesses = final_evaluation.get("weaknesses", [])
        risk_flags = final_evaluation.get("risk_flags", [])
        hire_recommendation = final_evaluation.get("hire_recommendation", "Unknown")
        brutal_summary = final_evaluation.get("brutal_summary", "")

        score_trend = transcript_data.get("score_trend", [])
        bluff_trend = transcript_data.get("bluff_trend", [])
        domain_strength = transcript_data.get("domain_strength", {})

        avg_live_score = round(sum(score_trend) / len(score_trend), 2) if score_trend else 0
        avg_bluff_risk = round(sum(bluff_trend) / len(bluff_trend), 2) if bluff_trend else 0

        return {
            "generated_at": datetime.utcnow().isoformat(),

            "executive_summary": {
                "overall_readiness": criterion_scores.get("overall_readiness", 0),
                "hire_recommendation": hire_recommendation,
                "average_live_score": avg_live_score,
                "average_bluff_risk": avg_bluff_risk
            },

            "detailed_scores": criterion_scores,

            "domain_strength_analysis": domain_strength,

            "resume_alignment_score": alignment_data.get("alignment_score", 0),

            "strengths": strengths,

            "weaknesses": weaknesses,

            "risk_flags": risk_flags,

            "brutal_summary": brutal_summary
        }
