from pydantic import BaseModel


class StartInterviewRequest(BaseModel):
    candidate_id: str
    resume_text: str
    job_role: str


class StartInterviewResponse(BaseModel):
    interview_id: str


class AnswerRequest(BaseModel):
    interview_id: str
    question: str
    answer: str


class EndInterviewResponse(BaseModel):
    candidate_id: str
    job_role: str
    metadata: dict
