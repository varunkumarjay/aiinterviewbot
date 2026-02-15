from fastapi import APIRouter, HTTPException
from ..models.schemas import (
    StartInterviewRequest,
    StartInterviewResponse,
    AnswerRequest,
    EndInterviewResponse
)
from ..services.interview_service import InterviewService

router = APIRouter()
interview_service = InterviewService()


@router.post("/start", response_model=StartInterviewResponse)
def start_interview(req: StartInterviewRequest):

    interview_id = interview_service.start_interview(
        req.candidate_id,
        req.resume_text,
        req.job_role
    )

    return StartInterviewResponse(interview_id=interview_id)


@router.post("/answer")
def answer_question(req: AnswerRequest):

    try:
        result = interview_service.process_answer(
            req.interview_id,
            req.question,
            req.answer
        )
        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/end/{interview_id}")
def end_interview(interview_id: str):
    return interview_service.end_interview(interview_id)
@router.post("/finalize")
def finalize_interview(payload: dict):

    interview_id = payload.get("interview_id")

    if not interview_id:
        raise HTTPException(status_code=400, detail="interview_id required")

    try:
        result = interview_service.finalize_interview(interview_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
