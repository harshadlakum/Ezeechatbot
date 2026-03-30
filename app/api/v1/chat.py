from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.db.repositories import BotRepository, MessageRepository
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag_pipeline import run_rag
from app.core.exceptions import BotNotFoundException
from app.utils.time_utils import Timer
from app.core.logging import logger

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
):
    bot_repo = BotRepository(db)
    bot = await bot_repo.get(request.bot_id)
    if not bot:
        raise BotNotFoundException(request.bot_id)

    history = [h.model_dump() for h in (request.conversation_history or [])]

    timer = Timer()
    timer.start()

    result = run_rag(
        bot_id=request.bot_id,
        user_message=request.user_message,
        conversation_history=history,
    )

    latency_ms = timer.elapsed_ms()

    msg_repo = MessageRepository(db)
    await msg_repo.create(
        bot_id=request.bot_id,
        user_message=request.user_message,
        response=result["answer"],
        latency_ms=latency_ms,
        input_tokens=result["input_tokens"],
        output_tokens=result["output_tokens"],
        cost_usd=result["cost_usd"],
        was_answered=result["was_answered"],
    )

    logger.info(
        f"Chat: bot_id={request.bot_id}, answered={result['was_answered']}, "
        f"latency={latency_ms}ms"
    )

    return ChatResponse(
        bot_id=request.bot_id,
        answer=result["answer"],
        was_answered=result["was_answered"],
        latency_ms=latency_ms,
        chunks_used=result["chunks_used"],
    )
