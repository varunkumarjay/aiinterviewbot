from sentence_transformers import SentenceTransformer

class EmbeddingService:

    def __init__(self):
        # 384 dimension model (matches your DB vector(384))
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed(self, text: str):
        embedding = self.model.encode(text)
        return embedding.tolist()
