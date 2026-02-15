from fastapi import APIRouter
from app.models.schemas import ResumeUploadRequest
from app.services.resume_service import ResumeService

router = APIRouter()
resume_service = ResumeService()


@router.post("/resume/process")
async def process_resume(request: ResumeUploadRequest):
    result = resume_service.process_resume(
        request.candidate_id,
        request.resume_text
    )
    return result
