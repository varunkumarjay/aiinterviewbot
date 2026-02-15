from core_engine.models.llm import LLM
import json


class QuestionGenerator:

    def __init__(self):
        self.llm = LLM()

    def generate_followup(
        self,
        role_profile,
        extraction_data,
        evaluation_data,
        difficulty_info
    ):

        overall_score = evaluation_data.get("overall_score", 0.5)
        depth_level = extraction_data.get("depth_level", 1)
        bluff_probability = difficulty_info.get("bluff_probability", 0.0)
        decision = difficulty_info.get("decision", "maintain")

        question_type = "maintain"

        if bluff_probability > 0.6:
            question_type = "precision_probe"

        elif overall_score > 0.7 and depth_level >= 2:
            question_type = "escalation"

        elif overall_score < 0.4:
            question_type = "clarification"

        elif depth_level <= 1:
            question_type = "deep_probe"

        prompt = f"""
You are a senior technical interviewer conducting a live interview.

Generate a follow-up question that sounds natural and human.

Question strategy:
{question_type}

Role Profile:
{json.dumps(role_profile, indent=2)}

Candidate Concepts Used:
{json.dumps(extraction_data.get("concepts_used", []), indent=2)}

Evaluation Summary:
{json.dumps(evaluation_data, indent=2)}

Rules:
- Ask only ONE question.
- Sound natural and conversational.
- Do not mention scoring.
- Focus on job role relevance.
- Push depth if weak.
- Escalate difficulty if strong.
- If bluff suspected, ask for specific implementation detail.
"""

        response = self.llm.generate(prompt, max_tokens=300)

        return {
            "question_type": question_type,
            "next_question": response.strip()
        }
