from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "EzeeChatBot"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    DATABASE_URL: str = "sqlite+aiosqlite:///./data/ezeechatbot.db"

    QDRANT_PATH: str = "./data/qdrant_storage"

    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384

    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5:3b"

    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 64
    RETRIEVAL_TOP_K: int = 5
    RELEVANCE_SCORE_THRESHOLD: float = 0.35

    COST_PER_1K_INPUT_TOKENS: float = 0.0
    COST_PER_1K_OUTPUT_TOKENS: float = 0.0

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
