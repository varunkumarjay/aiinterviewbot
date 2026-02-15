class SkillDepthSynthesizer:

    def __init__(self):
        pass

    def classify_depth(self, avg_depth):
        if avg_depth >= 4:
            return "Strong"
        elif avg_depth >= 3:
            return "Moderate"
        elif avg_depth >= 2:
            return "Surface"
        else:
            return "Weak"

    def analyze(
        self,
        role_profile: dict,
        alignment_data: dict,
        metadata: dict
    ):
        """
        Generate structured domain depth matrix.
        """

        core_domains = role_profile.get("core_domains", [])
        domain_strength = metadata.get("domain_strength", {})
        claimed_skills = alignment_data.get("claimed_skills", [])

        matrix = []
        weakness_clusters = []
        strength_clusters = []

        for domain in core_domains:
            avg_depth = domain_strength.get(domain, 0)
            classification = self.classify_depth(avg_depth)

            claimed = domain in claimed_skills

            risk = "Low"

            if claimed and avg_depth < 2.5:
                risk = "High"
                weakness_clusters.append(domain)
            elif avg_depth < 2:
                risk = "Moderate"
                weakness_clusters.append(domain)
            elif avg_depth >= 4:
                strength_clusters.append(domain)

            matrix.append({
                "domain": domain,
                "claimed_in_resume": claimed,
                "average_depth": round(avg_depth, 2),
                "classification": classification,
                "risk_level": risk
            })

        return {
            "skill_depth_matrix": matrix,
            "strength_clusters": strength_clusters,
            "weakness_clusters": weakness_clusters
        }