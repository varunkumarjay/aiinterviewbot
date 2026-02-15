class SkillGraphBuilder:

    def __init__(self):
        pass

    def build(self, role_profile):

        graph = {}

        for domain in role_profile.get("core_domains", []):
            graph[domain] = {
                "dependencies": [],
                "depth_required": 3
            }

        # Simple heuristic linking
        for domain in graph:
            if "system" in domain.lower():
                graph[domain]["dependencies"].append("architecture fundamentals")

            if "database" in domain.lower():
                graph[domain]["dependencies"].append("indexing")
                graph[domain]["dependencies"].append("transactions")

        return graph
