import json
import re


def extract_json_block(text: str):
    """
    Extract the first valid JSON object from model output.
    """
    try:
        match = re.search(r"\{.*?\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception:
        pass
    return None


def parse_evaluation_response(raw_text: str):
    """
    Safely parse structured evaluation JSON.
    Provides fallback if model output is malformed.
    """

    data = extract_json_block(raw_text)

    if not data:
        return {
            "conceptual_clarity": 2,
            "logical_structure": 2,
            "depth": 2,
            "practical_understanding": 2,
            "feedback": "Model output malformed. Assigned neutral baseline score."
        }

    # Defensive score validation
    def safe_score(val):
        try:
            val = int(val)
            return max(1, min(val, 5))
        except:
            return 2

    return {
        "conceptual_clarity": safe_score(data.get("conceptual_clarity", 2)),
        "logical_structure": safe_score(data.get("logical_structure", 2)),
        "depth": safe_score(data.get("depth", 2)),
        "practical_understanding": safe_score(data.get("practical_understanding", 2)),
        "feedback": data.get("feedback", "No detailed feedback provided.")
    }
