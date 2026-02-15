import uuid
from datetime import datetime

from core_engine.resume.role_intelligence_engine import RoleIntelligenceEngine
from core_engine.resume.alignment_engine import ResumeAlignmentEngine
from core_engine.interview.orchestrator import InterviewOrchestrator
from core_engine.post_analysis.deep_interview_evaluator import DeepInterviewEvaluator
from core_engine.post_analysis.admin_report_generator import AdminReportGenerator

from core_engine.embeddings.embedding_service import EmbeddingService
from core_engine.embeddings.similarity_engine import SimilarityEngine

from ..core.supabase_client import supabase


class InterviewService:

    def __init__(self):
        self.db = supabase
        self.deep_evaluator = DeepInterviewEvaluator()
        self.report_generator = AdminReportGenerator()
        self.embedder = EmbeddingService()
        self.similarity_engine = SimilarityEngine(self.db)

    # =========================================================
    # START INTERVIEW
    # =========================================================
    def start_interview(self, candidate_id, resume_text, job_role):

        role_engine = RoleIntelligenceEngine()
        alignment_engine = ResumeAlignmentEngine()

        role_profile = role_engine.build_role_profile(job_role)
        alignment_data = alignment_engine.analyze(resume_text, role_profile)

        interview_insert = self.db.table("interviews").insert({
            "candidate_id": candidate_id,
            "stage": "live",
            "difficulty_level": 1,
            "started_at": datetime.utcnow().isoformat(),
            "role_profile": role_profile,
            "alignment_data": alignment_data
        }).execute()

        interview_id = interview_insert.data[0]["id"]

        return interview_id

    # =========================================================
    # PROCESS ANSWER
    # =========================================================
    def process_answer(self, interview_id, question, answer):

        interview_row = self.db.table("interviews") \
            .select("*") \
            .eq("id", interview_id) \
            .single() \
            .execute()

        if not interview_row.data:
            raise ValueError("Invalid interview_id")

        if interview_row.data["stage"] != "live":
            raise ValueError("Interview is not active")

        role_profile = interview_row.data["role_profile"]
        alignment_data = interview_row.data["alignment_data"]
        candidate_id = interview_row.data["candidate_id"]

        # 🔥 Orchestrator evaluation
        orchestrator = InterviewOrchestrator(role_profile, alignment_data)
        result = orchestrator.process_answer(question, answer)

        # =====================================================
        # 🔥 NEW: Resume Similarity Intelligence
        # =====================================================
        answer_embedding = self.embedder.embed(answer)

        similarity_score = self.similarity_engine.compute_similarity(
            candidate_id,
            answer_embedding
        )

        # Reinforce bluff probability if mismatch
        if similarity_score < 0.3:
            result["bluff_probability"] = min(
                result.get("bluff_probability", 0) + 0.2,
                1.0
            )

        # =====================================================
        # Save transcript row
        # =====================================================
        self.db.table("interview_transcripts").insert({
            "interview_id": interview_id,
            "stage": "live",
            "question": question,
            "answer": answer,
            "evaluation": result,
            "similarity_score": similarity_score,
            "created_at": datetime.utcnow().isoformat()
        }).execute()

        # Attach similarity to API response
        result["similarity_score"] = similarity_score

        return result

    # =========================================================
    # END INTERVIEW
    # =========================================================
    def end_interview(self, interview_id):

        update = self.db.table("interviews") \
            .update({
                "stage": "completed",
                "completed_at": datetime.utcnow().isoformat()
            }) \
            .eq("id", interview_id) \
            .execute()

        if not update.data:
            raise ValueError("Invalid interview_id")

        return {
            "message": "Interview marked as completed",
            "interview_id": interview_id
        }

    # =========================================================
    # FINALIZE INTERVIEW
    # =========================================================
    def finalize_interview(self, interview_id):

        interview_row = self.db.table("interviews") \
            .select("*") \
            .eq("id", interview_id) \
            .single() \
            .execute()

        if not interview_row.data:
            raise ValueError("Invalid interview_id")

        if interview_row.data["stage"] != "completed":
            raise ValueError("Interview must be completed first")

        role_profile = interview_row.data["role_profile"]
        alignment_data = interview_row.data["alignment_data"]

        transcript_rows = self.db.table("interview_transcripts") \
            .select("*") \
            .eq("interview_id", interview_id) \
            .execute()

        transcript_data = {
            "answers": transcript_rows.data
        }

        # 🔥 Deep evaluation
        deep_result = self.deep_evaluator.evaluate_full_interview(
            transcript_data,
            role_profile,
            alignment_data
        )

        # 🔥 Admin report
        admin_report = self.report_generator.generate(
            deep_result,
            transcript_data,
            role_profile,
            alignment_data
        )

        # Save scorecard
        self.db.table("scorecards").insert({
            "interview_id": interview_id,
            "overall_score": deep_result.get("criterion_scores", {}).get("overall_readiness", 0),
            "technical_score": deep_result.get("criterion_scores", {}).get("skill_depth", 0),
            "communication_score": deep_result.get("criterion_scores", {}).get("career_clarity", 0),
            "resume_integrity_score": deep_result.get("criterion_scores", {}).get("bluff_risk", 0),
            "report": admin_report,
            "created_at": datetime.utcnow().isoformat()
        }).execute()

        return {
            "interview_id": interview_id,
            "deep_evaluation": deep_result,
            "admin_report": admin_report
        }

    # =========================================================
    # INDEX RESUME EMBEDDINGS
    # =========================================================
    def index_resume_embeddings(self, candidate_id, structured_resume_data):

        for section_name, content in structured_resume_data.items():

            if not content:
                continue

            text_block = f"{section_name}: {content}"

            embedding = self.embedder.embed(text_block)

            self.db.table("resume_embeddings").insert({
                "candidate_id": candidate_id,
                "content_type": section_name,
                "content_text": text_block,
                "embedding": embedding
            }).execute()
