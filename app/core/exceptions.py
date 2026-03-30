from fastapi import HTTPException


class BotNotFoundException(HTTPException):
    def __init__(self, bot_id: str):
        super().__init__(
            status_code=404,
            detail=f"Bot with id '{bot_id}' not found.",
        )


class IngestionException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail=detail)


class LLMException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=503, detail=f"LLM error: {detail}")


class EmbeddingException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=503, detail=f"Embedding error: {detail}")
