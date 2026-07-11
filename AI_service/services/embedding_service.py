from models.embedding import SearchResult
from vector.chromadb import ChromaVectorStore
from vector.pgvector import PgVectorStore


class EmbeddingService:
    def __init__(self) -> None:
        self.pgvector = PgVectorStore()
        self.chromadb = ChromaVectorStore()

    def search(self, query: str) -> list[SearchResult]:
        results = self.pgvector.search(query)
        if results:
            return results
        return self.chromadb.search(query)
