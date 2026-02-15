class DifficultyPolicy:

    def adjust_difficulty(
        self,
        role_profile,
        overall_score,
        depth_level,
        bluff_probability,
        vagueness_score
    ):

        # Defensive safety
        if role_profile is None:
            role_profile = {
                "difficulty_escalation_path": []
            }

        escalation_path = role_profile.get("difficulty_escalation_path", [])

        decision = "maintain"

        if overall_score > 0.7 and depth_level >= 2:
            decision = "increase"

        elif overall_score < 0.3 or bluff_probability > 0.6:
            decision = "decrease"

        next_topic = None
        if decision == "increase" and escalation_path:
            next_topic = escalation_path[0]

        return {
            "decision": decision,
            "next_topic": next_topic,
            "bluff_probability": bluff_probability,
            "vagueness": vagueness_score
        }
