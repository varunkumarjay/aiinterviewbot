from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingService:

    def __init__(self):
        self.model = SentenceTransformer("BAAI/bge-small-en-v1.5")

    def embed(self, text: str):
        vector = self.model.encode(text, normalize_embeddings=True)
        return vector.tolist()
