from core_engine.models.llm import LLM
import json
import re


class RoleIntelligenceEngine:

    def __init__(self):
        self.llm = LLM()

    def extract_json(self, text):
        try:
            # Grab only the LAST JSON block in the response
            start = text.rfind("{")
            end = text.rfind("}") + 1

            if start != -1 and end != -1:
                candidate = text[start:end]
                return json.loads(candidate)

        except Exception as e:
            print("JSON extraction failed:", e)

        return None


    def build_role_profile(self, job_role: str):

        prompt = f"""
You are a senior hiring architect.

Given the job role below, generate a structured role intelligence profile.

Return ONLY valid JSON in this format:

{{
  "core_domains": [],
  "expected_depth_areas": [],
  "critical_concepts": [],
  "bluff_sensitive_topics": [],
  "difficulty_escalation_path": [],
  "evaluation_weights": {{
      "clarity": 0.0,
      "logic": 0.0,
      "depth": 0.0,
      "application": 0.0,
      "resume_alignment": 0.0
  }}
}}

Job Role:
{job_role}
"""

        response = self.llm.generate(prompt, max_tokens=600)

        data = self.extract_json(response)

        if not data:
            print("WARNING: Role Intelligence JSON malformed. Using fallback.")
            return {
                "core_domains": ["Backend Fundamentals"],
                "expected_depth_areas": ["API Design", "Database Optimization"],
                "critical_concepts": ["REST", "Indexing", "Concurrency"],
                "bluff_sensitive_topics": [],
                "difficulty_escalation_path": [
                    "Basic APIs",
                    "Scalable Systems",
                    "Distributed Architecture"
                ],
                "evaluation_weights": {
                    "clarity": 0.2,
                    "logic": 0.2,
                    "depth": 0.2,
                    "application": 0.2,
                    "resume_alignment": 0.2
                }
            }

