from core_engine.models.llm import LLM
import json
import re


class ExtractionEngine:

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
            print("Extraction JSON parsing failed:", e)

        return None

    def analyze(self, role_profile, alignment_data, question, answer):

        prompt = f"""
You are a technical interviewer.

Analyze the candidate's answer.

Return ONLY valid JSON in this format:

{{
  "concepts_used": [],
  "depth_level": 1,
  "vagueness_score": 0.0,
  "confidence_level": 0.0,
  "matched_domains": []
}}

Question:
{question}

Answer:
{answer}

Role Profile:
{json.dumps(role_profile, indent=2)}

Resume Alignment:
{json.dumps(alignment_data, indent=2)}
"""

        response = self.llm.generate(prompt, max_tokens=800)

        print("\n===== EXTRACTION RAW RESPONSE =====\n")
        print(response)
        print("\n===================================\n")

        data = self.extract_json(response)

        if not data:
            print("WARNING: Extraction JSON malformed. Using fallback.")
            return {
                "concepts_used": [],
                "depth_level": 2,
                "vagueness_score": 0.5,
                "confidence_level": 0.5,
                "matched_domains": []
            }

        return data
