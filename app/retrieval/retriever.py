import os

from dotenv import load_dotenv
from fastembed import TextEmbedding
from qdrant_client import QdrantClient,models
from collections import defaultdict

from app.models.chunks import Chunk, ChunkMetadata

load_dotenv()

class Retriever:

    def __init__(self):

        self.client = QdrantClient(
            url = os.getenv("QDRANT_URL"),
            api_key = os.getenv("QDRANT_API_KEY")
        )

        self.collection_name = os.getenv("QDRANT_COLLECTION")

        # The same embedding model to embed the query:
        self.embedding_model = TextEmbedding(
            model_name = "sentence-transformers/all-MiniLM-L6-v2"
        )
    
    def _dense_search(self,query:str, top_k:int = 5):
        query_embedding = list(self.embedding_model.embed([query]))[0].tolist() # Converts the numpy array into list
        results = self.client.query_points(
            collection_name = self.collection_name,
            query = query_embedding,
            using  = "dense",
            limit = top_k
        ).points

        return results
    def _sparse_search(self,query:str, top_k:int = 5):
        results = self.client.query_points(
            collection_name=self.collection_name,
            using="sparse",
            query=models.Document(
                text=query,
                model="Qdrant/bm25",
            ),
            limit=top_k,
        ).points

        return results

    @staticmethod
    def _rrf(dense_results, sparse_results,k:int = 60):
        scores = defaultdict(float)
        points = {}

        # Dense ranking
        for rank, point in enumerate(dense_results, start=1):
            point_id = str(point.id)

            scores[point_id] += 1 / (k + rank)
            points[point_id] = point

        # Sparse ranking
        for rank, point in enumerate(sparse_results, start=1):
            point_id = str(point.id)

            scores[point_id] += 1 / (k + rank)
            points[point_id] = point

        ranked_ids = sorted(
            scores,
            key=scores.get,
            reverse=True,
        )

        return [points[point_id] for point_id in ranked_ids]

    def retrieve(self,query:str, top_k:int = 5)->list[Chunk]:

        dense_results = self._dense_search(query,top_k*2)
        sparse_results = self._sparse_search(query,top_k*2)

        fused = self._rrf(
            dense_results,
            sparse_results
        )

        results = []

        for point in fused[:top_k]:

            payload = point.payload

            metadata = ChunkMetadata(
                chunk_id=payload["chunk_id"],
                document_id=payload["document_id"],
                title=payload["title"],
                department=payload["department"],
                category=payload["category"],
                version=payload["version"],
                section=payload["section"],
                subsection=payload.get("subsection"),
                heading_path=payload["heading_path"],
                heading_level=payload["heading_level"],
                chunk_index=payload["chunk_index"],
                tags=payload["tags"],
            )

            results.append(
                Chunk(
                    metadata=metadata,
                    content=payload["content"],
                    source=payload["source"],
                )
            )

        return results

        
    

if __name__ == "__main__":
    retriever = Retriever()

    chunks = retriever.retrieve(
        "What is the standard refund window for subscription services?",
        top_k=5,
    )

    for i, chunk in enumerate(chunks, start=1):
        heading_path = " > ".join(chunk.metadata.heading_path)
        print(f"\nResult {i}")
        print(f"Title: {chunk.metadata.title}")
        print(f"Section: {heading_path}")
        print(chunk.content)
        print("-" * 80)