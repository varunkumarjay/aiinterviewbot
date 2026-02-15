from datetime import datetime


class MetadataStore:

    def __init__(self):
        self.answers = []
        self.score_history = []
        self.bluff_history = []
        self.difficulty_history = []
        self.domain_strength = {}

    def add_entry(
        self,
        question: str,
        extraction_data: dict,
        evaluation_data: dict,
        bluff_probability: float,
        difficulty_info: dict
    ):

        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "question": question,
            "extraction": extraction_data,
            "evaluation": evaluation_data,
            "bluff_probability": bluff_probability,
            "difficulty": difficulty_info
        }

        self.answers.append(entry)

        # Track trends
        self.score_history.append(
            evaluation_data.get("overall_score", 0)
        )

        self.bluff_history.append(bluff_probability)

        # Track difficulty decision instead of numeric level
        self.difficulty_history.append(
            difficulty_info.get("decision", "maintain")
        )

        # Track domain performance
        matched_domains = extraction_data.get("matched_domains", [])
        depth = extraction_data.get("depth_level", 0)

        for domain in matched_domains:
            if domain not in self.domain_strength:
                self.domain_strength[domain] = []

            self.domain_strength[domain].append(depth)

    def get_score_trend(self):
        return self.score_history

    def get_bluff_trend(self):
        return self.bluff_history

    def get_difficulty_trend(self):
        return self.difficulty_history

    def get_domain_strength_summary(self):
        summary = {}

        for domain, depths in self.domain_strength.items():
            avg_depth = sum(depths) / len(depths)
            summary[domain] = round(avg_depth, 2)

        return summary

    def get_full_metadata(self):
        return {
            "answers": self.answers,
            "score_trend": self.score_history,
            "bluff_trend": self.bluff_history,
            "difficulty_trend": self.difficulty_history,
            "domain_strength": self.get_domain_strength_summary()
        }
