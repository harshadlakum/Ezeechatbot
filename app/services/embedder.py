from sentence_transformers import SentenceTransformer
from typing import List
from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()

_model: SentenceTransformer = None


def get_embedder() -> SentenceTransformer:
    global _model
    if _model is None:
        logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _model


def embed_texts(texts: List[str]) -> List[List[float]]:
    model = get_embedder()
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    return embeddings.tolist()


def embed_query(query: str) -> List[float]:
    return embed_texts([query])[0]
