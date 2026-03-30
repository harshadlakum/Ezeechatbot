from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories import MessageRepository, BotRepository
from app.schemas.stats import StatsResponse
from app.core.exceptions import BotNotFoundException


async def get_bot_stats(bot_id: str, db: AsyncSession) -> StatsResponse:
    bot_repo = BotRepository(db)
    bot = await bot_repo.get(bot_id)
    if not bot:
        raise BotNotFoundException(bot_id)
    msg_repo = MessageRepository(db)
    stats = await msg_repo.get_stats(bot_id)
    return StatsResponse(
        bot_id=bot_id,
        total_messages_served=stats["total_messages"],
        average_response_latency_ms=stats["avg_latency_ms"],
        estimated_token_cost_usd=stats["total_cost_usd"],
        unanswered_questions=stats["unanswered_count"],
    )
