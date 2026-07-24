from pathlib import Path
import uuid

import frontmatter
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models
from qdrant_client.models import (
    Distance,
    SparseVectorParams,
    VectorParams,
)

from app.ingestion.chunker import DocumentChunker
from app.models.documents import Document, DocumentMetadata

from tqdm import tqdm
from qdrant_client.models import PointStruct
from fastembed import TextEmbedding



load_dotenv()

from os import getenv

QDRANT_URL = getenv("QDRANT_URL")
QDRANT_API_KEY = getenv("QDRANT_API_KEY")
COLLECTION_NAME = getenv("QDRANT_COLLECTION")


KNOWLEDGE_BASE_PATH = Path("documents")


client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

chunker = DocumentChunker()

embedding_model = TextEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

def create_collection() -> None:
    """
    Creates the Qdrant collection if it doesn't already exist.
    """

    collections = client.get_collections().collections

    collection_names = [collection.name for collection in collections]

    if COLLECTION_NAME in collection_names:
        print(f"Collection '{COLLECTION_NAME}' already exists.")
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={
            "dense": VectorParams(
                size=384,
                distance=Distance.COSINE,
            )
        },
        sparse_vectors_config={
            "sparse": models.SparseVectorParams(
                modifier=models.Modifier.IDF
            )
        },
    )

    print(f"Created collection '{COLLECTION_NAME}'.")

def load_documents() -> list[Document]:
    """
    Loads all markdown documents from the knowledge base.
    """

    documents: list[Document] = []

    markdown_files = sorted(KNOWLEDGE_BASE_PATH.glob("*.md"))

    for file_path in markdown_files:

        post = frontmatter.load(file_path)

        metadata = DocumentMetadata(
            document_id=post["document_id"],
            title=post["title"],
            department=post["department"],
            category=post["category"],
            version=str(post["version"]),   # <-- Fix
            owner=post["owner"],
            last_updated=post["last_updated"],
            tags=post["tags"],
        )

        document = Document(
            metadata=metadata,
            content=post.content,
            source=file_path,
        )

        documents.append(document)

    print(f"Loaded {len(documents)} documents.")

    return documents

def create_chunks(documents: list[Document]):
    """
    Converts all documents into chunks.
    """

    all_chunks = []

    for document in documents:
        chunks = chunker.chunk(document)
        all_chunks.extend(chunks)

    print(f"Generated {len(all_chunks)} chunks.")

    return all_chunks

def upload_chunks(chunks):
    """
    Generate embeddings and upload chunks to Qdrant.
    """

    print("Generating embeddings...")

    texts = [chunk.content for chunk in chunks]

    embeddings = list(embedding_model.embed(texts))

    print("Uploading to Qdrant...")

    points = []

    for chunk, embedding in tqdm(
        zip(chunks, embeddings),
        total=len(chunks)
    ):

        payload = {
            "chunk_id": chunk.metadata.chunk_id,
            "document_id": chunk.metadata.document_id,
            "title": chunk.metadata.title,
            "department": chunk.metadata.department,
            "category": chunk.metadata.category,
            "version": chunk.metadata.version,
            "section": chunk.metadata.section,
            "subsection": chunk.metadata.subsection,
            "heading_path": chunk.metadata.heading_path,
            "heading_level": chunk.metadata.heading_level,
            "chunk_index": chunk.metadata.chunk_index,
            "tags": chunk.metadata.tags,
            "content": chunk.content,
            "source": str(chunk.source),
        }

        points.append(
            PointStruct(
                id=uuid.uuid5(
                    uuid.NAMESPACE_DNS,
                    chunk.metadata.chunk_id
                ),
                vector={
                    "dense": embedding.tolist(),
                    "sparse": models.Document(
                        text=chunk.content,
                        model="Qdrant/bm25",
                    ),
                },
                payload=payload,
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
        wait=True,
    )

    print(f"Uploaded {len(points)} chunks.")


if __name__ == "__main__":
    create_collection()

    documents = load_documents()

    chunks = create_chunks(documents)

    upload_chunks(chunks)