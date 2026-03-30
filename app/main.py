import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.logging import logger
from app.db.session import init_db
from app.api.v1 import health, upload, chat, stats

settings = get_settings()

os.makedirs("./data", exist_ok=True)
os.makedirs("./data/qdrant_storage", exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting EzeeChatBot API...")
    await init_db()
    logger.info("Database initialised.")
    yield
    logger.info("Shutting down EzeeChatBot API.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="RAG Chatbot API - answers questions from uploaded knowledge bases.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PREFIX = "/api/v1"

app.include_router(health.router, prefix=PREFIX, tags=["Health"])
app.include_router(upload.router, prefix=PREFIX, tags=["Upload"])
app.include_router(chat.router, prefix=PREFIX, tags=["Chat"])
app.include_router(stats.router, prefix=PREFIX, tags=["Stats"])
