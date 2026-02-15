from core_engine.interview.extraction_engine import ExtractionEngine
from core_engine.interview.live_evaluator import LiveEvaluator
from core_engine.interview.bluff_detector import BluffDetector
from core_engine.interview.difficulty_policy import DifficultyPolicy
from core_engine.interview.metadata_store import MetadataStore
from core_engine.interview.question_generator import QuestionGenerator


class InterviewOrchestrator:

    def __init__(self, role_profile, alignment_data):
        self.role_profile = role_profile
        self.alignment_data = alignment_data

        self.extraction_engine = ExtractionEngine()
        self.live_evaluator = LiveEvaluator()
        self.bluff_detector = BluffDetector()
        self.difficulty_policy = DifficultyPolicy()
        self.metadata_store = MetadataStore()

        self.question_generator = QuestionGenerator()


    def process_answer(self, question, answer):

        # 1️⃣ Extraction
        extraction_data = self.extraction_engine.analyze(
            self.role_profile,
            self.alignment_data,
            question,
            answer
        )

        # 2️⃣ Live evaluation
        evaluation_data = self.live_evaluator.evaluate(
            self.role_profile,
            self.alignment_data,
            extraction_data,
            question,
            answer
        )

        # 3️⃣ Bluff detection
        bluff_probability = self.bluff_detector.compute_bluff_probability(
            extraction_data,
            evaluation_data,
            self.role_profile
        )

        # 4️⃣ Difficulty adjustment
        difficulty_info = self.difficulty_policy.adjust_difficulty(
            self.role_profile,
            evaluation_data.get("overall_score", 0.5),
            extraction_data.get("depth_level", 1),
            bluff_probability,
            extraction_data.get("vagueness_score", 0.5)
        )

        # 5️⃣ Store metadata
        self.metadata_store.add_entry(
            question,
            extraction_data,
            evaluation_data,
            bluff_probability,
            difficulty_info
        )

        followup = self.question_generator.generate_followup(
            self.role_profile,
            extraction_data,
            evaluation_data,
            difficulty_info
        )

        # 6️⃣ Generate follow-up question
        followup = self.question_generator.generate_followup(
            self.role_profile,
            extraction_data,
            evaluation_data,
            difficulty_info
        )

        return {
            "extraction": extraction_data,
            "evaluation": evaluation_data,
            "bluff_probability": bluff_probability,
            "difficulty": difficulty_info,
            "followup": followup
        }

    def get_metadata(self):
        return self.metadata_store.get_full_metadata()
