class BiasAudit:

    def __init__(self):
        pass

    def analyze(self, metadata, recommendation_data):

        score_trend = metadata.get("score_trend", [])
        bluff_trend = metadata.get("bluff_trend", [])

        if not score_trend:
            return {}

        avg_score = sum(score_trend) / len(score_trend)

        bias_flags = []

        # Excessively harsh scoring
        if avg_score < 1.8:
            bias_flags.append("Evaluation extremely harsh. Review scoring balance.")

        # Suspiciously perfect scoring
        if avg_score > 4.8:
            bias_flags.append("Evaluation unusually lenient.")

        # Consistent high bluff detection
        if sum(bluff_trend)/len(bluff_trend) > 0.8:
            bias_flags.append("Bluff detection consistently high. Possible over-penalization.")

        bias_risk = "Low"
        if len(bias_flags) >= 2:
            bias_risk = "Moderate"
        if len(bias_flags) >= 3:
            bias_risk = "High"

        return {
            "bias_flags": bias_flags,
            "bias_risk_level": bias_risk
        }
