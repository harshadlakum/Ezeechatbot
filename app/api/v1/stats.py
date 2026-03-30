from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.stats_service import get_bot_stats
from app.schemas.stats import StatsResponse

router = APIRouter()


@router.get("/stats/{bot_id}", response_model=StatsResponse)
async def stats(bot_id: str, db: AsyncSession = Depends(get_db)):
    return await get_bot_stats(bot_id, db)
