from typing import List, Dict, Any
from app.services.embedder import embed_query
from app.services.vector_store import search_chunks
from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()


def retrieve_relevant_chunks(
    query: str,
    bot_id: str,
    top_k: int = None,
) -> List[Dict[str, Any]]:
    if top_k is None:
        top_k = settings.RETRIEVAL_TOP_K
    query_embedding = embed_query(query)
    results = search_chunks(query_embedding, bot_id, top_k)
    threshold = settings.RELEVANCE_SCORE_THRESHOLD
    filtered = [r for r in results if r["score"] >= threshold]
    logger.info(
        f"Retrieved {len(results)} chunks, {len(filtered)} passed threshold "
        f"{threshold} for bot_id={bot_id}"
    )
    return filtered
