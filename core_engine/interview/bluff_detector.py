class BluffDetector:

    def compute_bluff_probability(self, extraction_data, evaluation_data, role_profile):
        """
        Simple heuristic bluff detection logic.
        Later this can become LLM-based.
        """

        vagueness = extraction_data.get("vagueness_score", 0.5)
        depth = extraction_data.get("depth_level", 1)
        confidence = extraction_data.get("confidence_level", 0.5)

        clarity = evaluation_data.get("clarity", 0.5)
        logic = evaluation_data.get("logic", 0.5)

        # Basic heuristic logic
        bluff_score = 0.0

        # High confidence + low depth = possible bluff
        if confidence > 0.7 and depth <= 1:
            bluff_score += 0.4

        # High vagueness increases bluff likelihood
        bluff_score += vagueness * 0.3

        # Low clarity + low logic increases bluff
        if clarity < 0.4 and logic < 0.4:
            bluff_score += 0.3

        return min(bluff_score, 1.0)
