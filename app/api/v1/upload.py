from fastapi import APIRouter, UploadFile, File, Form, Depends
from typing import Optional, Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.db.repositories import BotRepository
from app.schemas.upload import UploadResponse
from app.services.pdf_loader import load_pdf
from app.services.url_loader import load_url
from app.services.text_loader import load_text
from app.services.chunker import chunk_text
from app.services.embedder import embed_texts
from app.services.vector_store import store_chunks
from app.utils.hashing import generate_bot_id
from app.core.exceptions import IngestionException
from app.core.logging import logger

router = APIRouter()


@router.post("/upload", response_model=UploadResponse)
async def upload_knowledge_base(
    source_type: Annotated[str, Form(description="text | url | pdf")],
    text: Annotated[Optional[str], Form()] = None,
    url: Annotated[Optional[str], Form()] = None,
    file: Annotated[Optional[UploadFile], File()] = None,
    db: AsyncSession = Depends(get_db),
):
    bot_id = generate_bot_id()
    raw_text = ""

    try:
        if source_type == "text":
            if not text:
                raise IngestionException("'text' field is required for source_type='text'.")
            raw_text = load_text(text)

        elif source_type == "url":
            if not url:
                raise IngestionException("'url' field is required for source_type='url'.")
            raw_text = load_url(url)

        elif source_type == "pdf":
            if file is None:
                raise IngestionException("'file' is required for source_type='pdf'.")
            file_bytes = await file.read()
            if not file_bytes:
                raise IngestionException("Uploaded file is empty.")
            raw_text = load_pdf(file_bytes)

        else:
            raise IngestionException(
                f"Invalid source_type '{source_type}'. Use: text, url, pdf."
            )

    except IngestionException:
        raise
    except Exception as e:
        raise IngestionException(str(e))

    if not raw_text.strip():
        raise IngestionException("Extracted content is empty.")

    chunks = chunk_text(raw_text, bot_id=bot_id, source_type=source_type)
    if not chunks:
        raise IngestionException("Chunking produced no results.")

    texts = [c["text"] for c in chunks]
    embeddings = embed_texts(texts)
    store_chunks(chunks, embeddings, bot_id)

    bot_repo = BotRepository(db)
    await bot_repo.create(
        bot_id=bot_id,
        source_type=source_type,
        chunks_stored=len(chunks),
    )

    logger.info(f"Bot created: bot_id={bot_id}, source={source_type}, chunks={len(chunks)}")

    return UploadResponse(
        bot_id=bot_id,
        source_type=source_type,
        chunks_stored=len(chunks),
        message=f"Knowledge base created successfully with {len(chunks)} chunks.",
    )
