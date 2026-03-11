from sentence_transformers import SentenceTransformer

class Embedder:
    """
    Converts text chunks into embeddings.
    """

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts):
        """
        Generate embeddings for a list of texts.
        """
        embeddings = self.model.encode(texts)
        return embeddings