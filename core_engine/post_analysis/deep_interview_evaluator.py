from core_engine.models.llm import LLM
import json
import re


class DeepInterviewEvaluator:

    def __init__(self):
        self.llm = LLM()

    def _extract_json(self, text: str):
        """
        Safely extract the FIRST valid JSON object from model response.
        More robust against extra commentary and nested braces.
        """
        try:
            # Find all possible JSON-like blocks
            candidates = re.findall(r"\{[\s\S]*?\}", text)

            for candidate in candidates:
                try:
                    return json.loads(candidate)
                except json.JSONDecodeError:
                    continue

        except Exception as e:
            print("Deep evaluation JSON extraction error:", e)

        return None

    def evaluate_full_interview(
        self,
        transcript_data: dict,
        role_profile: dict,
        alignment_data: dict
    ):

        prompt = f"""
You are a senior hiring committee member.

You are analyzing a completed technical interview.

Evaluate the candidate across these dimensions:

1. Background relevance to role
2. Career clarity and motivation
3. Skill authenticity and depth
4. Project understanding and contribution clarity
5. Logical reasoning ability
6. Conceptual clarity
7. Practical feasibility thinking
8. Application of knowledge
9. Risk of exaggeration or bluff
10. Overall hire readiness

Be strict but fair.
Use evidence from transcript.

Return ONLY valid JSON in this format:

{{
  "criterion_scores": {{
      "background_relevance": 0.0,
      "career_clarity": 0.0,
      "skill_depth": 0.0,
      "project_understanding": 0.0,
      "logical_reasoning": 0.0,
      "conceptual_clarity": 0.0,
      "practical_feasibility": 0.0,
      "application_ability": 0.0,
      "bluff_risk": 0.0,
      "overall_readiness": 0.0
  }},
  "strengths": [],
  "weaknesses": [],
  "risk_flags": [],
  "hire_recommendation": "",
  "brutal_summary": ""
}}

Transcript:
{json.dumps(transcript_data, indent=2)}

Role Profile:
{json.dumps(role_profile, indent=2)}

Resume Alignment:
{json.dumps(alignment_data, indent=2)}
"""

        response = self.llm.generate(prompt, max_tokens=1500)

        print("\n===== DEEP EVALUATION RAW RESPONSE =====\n")
        print(response)
        print("\n========================================\n")

        data = self._extract_json(response)

        if not data:
            print("Deep evaluation parsing failed.")
            return {
                "error": "Deep evaluation parsing failed",
                "raw_response": response
            }

        return data
