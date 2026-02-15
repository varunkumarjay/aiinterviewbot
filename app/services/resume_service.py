from app.core.supabase_client import supabase
from app.services.embedding_service import EmbeddingService
import json

class ResumeService:

    def __init__(self):
        self.embedding_service = EmbeddingService()

    def parse_resume(self, resume_text: str):
        """
        Replace this with LLaMA call later.
        For now simple structured simulation.
        """
        structured = {
            "skills": ["Python", "Django", "PostgreSQL"],
            "projects": [],
            "experience": [],
            "career_goal": "",
            "soft_skills": []
        }
        return structured

    def store_structured_resume(self, candidate_id, structured_data):
        return supabase.table("resumes_structured").insert({
            "candidate_id": candidate_id,
            "structured_data": structured_data
        }).execute()

    def store_embeddings(self, candidate_id, structured_data):

        embeddings_to_store = []

        # Embed skills
        for skill in structured_data.get("skills", []):
            vector = self.embedding_service.embed(skill)

            embeddings_to_store.append({
                "candidate_id": candidate_id,
                "content_type": "skill",
                "content_text": skill,
                "embedding": vector
            })

        if embeddings_to_store:
            supabase.table("resume_embeddings").insert(
                embeddings_to_store
            ).execute()

    def process_resume(self, candidate_id, resume_text):

        structured_data = self.parse_resume(resume_text)

        self.store_structured_resume(candidate_id, structured_data)
        self.store_embeddings(candidate_id, structured_data)

        return {"status": "resume_processed"}
