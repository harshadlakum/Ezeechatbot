import os
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)
from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()

COLLECTION_NAME = "ezeechatbot_chunks"

_client: QdrantClient = None


def get_qdrant_client() -> QdrantClient:
    global _client
    if _client is None:
        os.makedirs(settings.QDRANT_PATH, exist_ok=True)
        _client = QdrantClient(path=settings.QDRANT_PATH)
        logger.info(f"Qdrant client initialised at: {settings.QDRANT_PATH}")
    return _client


def ensure_collection():
    client = get_qdrant_client()
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=settings.EMBEDDING_DIMENSION,
                distance=Distance.COSINE,
            ),
        )
        logger.info(f"Created Qdrant collection: {COLLECTION_NAME}")


def store_chunks(
    chunks: List[Dict[str, Any]],
    embeddings: List[List[float]],
    bot_id: str,
):
    ensure_collection()
    client = get_qdrant_client()
    points = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        point_id = abs(hash(f"{bot_id}_{i}")) % (2**31)
        points.append(
            PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "bot_id": bot_id,
                    "text": chunk["text"],
                    **chunk["metadata"],
                },
            )
        )
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    logger.info(f"Stored {len(points)} vectors for bot_id={bot_id}")


def search_chunks(
    query_embedding: List[float],
    bot_id: str,
    top_k: int,
) -> List[Dict[str, Any]]:
    ensure_collection()
    client = get_qdrant_client()
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="bot_id",
                    match=MatchValue(value=bot_id),
                )
            ]
        ),
        limit=top_k,
        with_payload=True,
    )
    return [
        {
            "text": r.payload.get("text", ""),
            "score": r.score,
            "chunk_index": r.payload.get("chunk_index", 0),
        }
        for r in results
    ]
