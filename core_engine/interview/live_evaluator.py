from core_engine.models.llm import LLM
import json
import re


class LiveEvaluator:

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
            print("Live evaluation JSON parsing failed:", e)

        return None

    def evaluate(self, role_profile, alignment_data, extraction_data, question, answer):

        prompt = f"""
You are a senior technical interviewer.

Evaluate the candidate's answer.

Return ONLY valid JSON in this format:

{{
  "clarity": 0.0,
  "logic": 0.0,
  "depth": 0.0,
  "application": 0.0,
  "overall_score": 0.0,
  "feedback": ""
}}

Question:
{question}

Answer:
{answer}

Extracted Analysis:
{json.dumps(extraction_data, indent=2)}

Role Profile:
{json.dumps(role_profile, indent=2)}
"""

        response = self.llm.generate(prompt, max_tokens=800)

        print("\n===== LIVE EVALUATION RAW RESPONSE =====\n")
        print(response)
        print("\n========================================\n")

        data = self.extract_json(response)

        if not data:
            print("WARNING: Live evaluation JSON malformed. Using fallback.")
            return {
                "clarity": 0.5,
                "logic": 0.5,
                "depth": 0.5,
                "application": 0.5,
                "overall_score": 0.5,
                "feedback": "Evaluation fallback used."
            }

        return data
