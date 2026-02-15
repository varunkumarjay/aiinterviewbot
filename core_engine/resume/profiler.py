from core_engine.models.llm import LLM
from core_engine.utils.prompts import RESUME_PROFILING_PROMPT

class ResumeProfiler:

    def __init__(self):
        self.llm = LLM()

    def build_profile(self, resume_text, job_role):
        prompt = RESUME_PROFILING_PROMPT.format(
            resume=resume_text,
            role=job_role
        )
        return self.llm.generate(prompt)
