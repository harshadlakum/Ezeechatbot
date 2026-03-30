from pydantic import BaseModel
from typing import List, Optional


class ConversationTurn(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    bot_id: str
    user_message: str
    conversation_history: Optional[List[ConversationTurn]] = []


class ChatResponse(BaseModel):
    bot_id: str
    answer: str
    was_answered: bool
    latency_ms: float
    chunks_used: int
