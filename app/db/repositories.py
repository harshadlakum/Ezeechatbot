from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, Integer, cast, case
from app.db.models import BotRecord, MessageRecord


class BotRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, bot_id: str, source_type: str, chunks_stored: int) -> BotRecord:
        bot = BotRecord(
            bot_id=bot_id,
            source_type=source_type,
            chunks_stored=chunks_stored,
        )
        self.db.add(bot)
        await self.db.commit()
        await self.db.refresh(bot)
        return bot

    async def get(self, bot_id: str) -> BotRecord | None:
        result = await self.db.execute(
            select(BotRecord).where(BotRecord.bot_id == bot_id)
        )
        return result.scalar_one_or_none()


class MessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        bot_id: str,
        user_message: str,
        response: str,
        latency_ms: float,
        input_tokens: int,
        output_tokens: int,
        cost_usd: float,
        was_answered: bool,
    ) -> MessageRecord:
        record = MessageRecord(
            bot_id=bot_id,
            user_message=user_message,
            response=response,
            latency_ms=latency_ms,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost_usd,
            was_answered=1 if was_answered else 0,
        )
        self.db.add(record)
        await self.db.commit()
        return record

    async def get_stats(self, bot_id: str) -> dict:
        result = await self.db.execute(
            select(
                func.count(MessageRecord.id).label("total_messages"),
                func.avg(MessageRecord.latency_ms).label("avg_latency_ms"),
                func.sum(MessageRecord.cost_usd).label("total_cost_usd"),
                func.sum(
                    case(
                        (MessageRecord.was_answered == 0, 1),
                        else_=0
                    )
                ).label("unanswered_count"),
            ).where(MessageRecord.bot_id == bot_id)
        )
        row = result.one()
        return {
            "total_messages": row.total_messages or 0,
            "avg_latency_ms": round(row.avg_latency_ms or 0.0, 2),
            "total_cost_usd": round(row.total_cost_usd or 0.0, 6),
            "unanswered_count": int(row.unanswered_count or 0),
        }
