class CrossAnswerPatternAnalyzer:

    def __init__(self):
        pass

    def analyze(self, metadata: dict):

        score_trend = metadata.get("score_trend", [])
        bluff_trend = metadata.get("bluff_trend", [])
        difficulty_trend = metadata.get("difficulty_trend", [])

        if not score_trend:
            return {}

        avg_score = sum(score_trend) / len(score_trend)
        score_variance = max(score_trend) - min(score_trend)

        # 1️⃣ Performance stability
        if score_variance < 0.5:
            stability = "Stable"
        elif score_variance < 1.5:
            stability = "Moderately Variable"
        else:
            stability = "Highly Unstable"

        # 2️⃣ Performance direction
        if score_trend[-1] > score_trend[0]:
            trajectory = "Improving"
        elif score_trend[-1] < score_trend[0]:
            trajectory = "Declining"
        else:
            trajectory = "Flat"

        # 3️⃣ Difficulty response analysis
        collapse_under_difficulty = False
        if len(score_trend) > 1:
            for i in range(1, len(score_trend)):
                if difficulty_trend[i] > difficulty_trend[i - 1] and score_trend[i] < score_trend[i - 1] - 1:
                    collapse_under_difficulty = True
                    break

        # 4️⃣ Bluff consistency
        avg_bluff = sum(bluff_trend) / len(bluff_trend) if bluff_trend else 0

        if avg_bluff > 0.6:
            bluff_pattern = "Consistently High Bluff Risk"
        elif avg_bluff > 0.3:
            bluff_pattern = "Moderate Bluff Risk"
        else:
            bluff_pattern = "Low Bluff Risk"

        return {
            "average_score": round(avg_score, 2),
            "performance_stability": stability,
            "performance_trajectory": trajectory,
            "collapse_under_difficulty": collapse_under_difficulty,
            "bluff_pattern": bluff_pattern
        }
