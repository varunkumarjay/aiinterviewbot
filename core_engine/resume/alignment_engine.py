from core_engine.models.llm import LLM
import json
import re


class ResumeAlignmentEngine:

    def __init__(self):
        self.llm = LLM()

    def extract_json(self, text):
        try:
            start = text.rfind("{")
            end = text.rfind("}") + 1

            if start != -1 and end != -1:
                candidate = text[start:end]
                return json.loads(candidate)

        except Exception as e:
            print("Alignment JSON extraction failed:", e)

        return None

    def analyze(self, resume_text: str, role_profile: dict):

        prompt = f"""
You are an expert recruiter.

Analyze the candidate resume against the role profile.

Return ONLY valid JSON in this format:

{{
  "claimed_skills": [],
  "matched_domains": [],
  "missing_domains": [],
  "alignment_score": 0.0
}}

Resume:
{resume_text}

Role Profile:
{json.dumps(role_profile, indent=2)}
"""

        response = self.llm.generate(prompt, max_tokens=800)

        print("\n===== ALIGNMENT RAW RESPONSE =====\n")
        print(response)
        print("\n==================================\n")

        data = self.extract_json(response)

        if not data:
            print("WARNING: Resume Alignment JSON malformed. Using fallback.")
            return {
                "claimed_skills": [],
                "matched_domains": [],
                "missing_domains": [],
                "alignment_score": 0.5
            }

        return data
