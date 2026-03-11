class Retriever:
    """
    Retrieves relevant text chunks from the vector database.
    """

    def __init__(self, vector_store, embedder):
        self.vector_store = vector_store
        self.embedder = embedder

    def retrieve(self, query, top_k=3):
        # Convert query to embedding
        query_embedding = self.embedder.embed_texts([query])

        # Search in vector database
        results = self.vector_store.search(query_embedding, top_k)

        return results