import re
import json


def clean_llm_output(text: str) -> str:
    """
    Removes extra prompt echoes or junk text from LLM output.
    """
    return text.strip()


def extract_json(text: str):
    """
    Extract JSON block from model output safely.
    """
    try:
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception:
        pass
    return None


def clamp_score(value, min_val=1, max_val=5):
    try:
        value = int(value)
        return max(min_val, min(value, max_val))
    except:
        return min_val
