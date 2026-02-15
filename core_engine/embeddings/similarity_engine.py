import numpy as np
import json


class SimilarityEngine:

    def __init__(self, db):
        self.db = db

    def compute_similarity(self, candidate_id: str, answer_embedding: list):

        rows = self.db.table("resume_embeddings") \
            .select("embedding") \
            .eq("candidate_id", candidate_id) \
            .execute()

        if not rows.data:
            return 0.0

        answer_vec = np.array(answer_embedding, dtype=float)

        max_similarity = 0.0

        for row in rows.data:

            # 🔥 Convert string vector → actual list
            embedding_raw = row["embedding"]

            if isinstance(embedding_raw, str):
                resume_list = json.loads(embedding_raw)
            else:
                resume_list = embedding_raw

            resume_vec = np.array(resume_list, dtype=float)

            similarity = self._cosine_similarity(answer_vec, resume_vec)

            if similarity > max_similarity:
                max_similarity = similarity

        return float(max_similarity)

    def cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
