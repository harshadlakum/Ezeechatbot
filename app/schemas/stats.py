from pydantic import BaseModel


class StatsResponse(BaseModel):
    bot_id: str
    total_messages_served: int
    average_response_latency_ms: float
    estimated_token_cost_usd: float
    unanswered_questions: int
