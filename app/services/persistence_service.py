from app.core.supabase_client import supabase


class PersistenceService:

    def create_interview(self, interview_id, candidate_id, job_role):

        supabase.table("interviews").insert({
            "id": interview_id,
            "candidate_id": candidate_id,
            "job_role": job_role,
            "status": "active"
        }).execute()

    def save_transcript_entry(self, interview_id, question, answer, evaluation_json):

        supabase.table("transcripts").insert({
            "interview_id": interview_id,
            "question": question,
            "answer": answer,
            "evaluation_json": evaluation_json
        }).execute()

    def save_metadata(self, interview_id, metadata_json):

        supabase.table("interview_metadata").upsert({
            "interview_id": interview_id,
            "metadata_json": metadata_json
        }).execute()

    def save_admin_report(self, interview_id, report_json):

        supabase.table("admin_reports").insert({
            "interview_id": interview_id,
            "report_json": report_json
        }).execute()

    def complete_interview(self, interview_id):

        supabase.table("interviews").update({
            "status": "completed"
        }).eq("id", interview_id).execute()
