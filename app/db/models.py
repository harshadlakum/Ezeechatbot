from sqlalchemy import Column, String, Integer, Float, DateTime, func
from app.db.session import Base


class BotRecord(Base):
    __tablename__ = "bots"

    bot_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)
    source_type = Column(String, nullable=False)
    chunks_stored = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())


class MessageRecord(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    bot_id = Column(String, index=True, nullable=False)
    user_message = Column(String, nullable=False)
    response = Column(String, nullable=False)
    latency_ms = Column(Float, nullable=False)
    input_tokens = Column(Integer, default=0)
    output_tokens = Column(Integer, default=0)
    cost_usd = Column(Float, default=0.0)
    was_answered = Column(Integer, default=1)
    created_at = Column(DateTime, server_default=func.now())
