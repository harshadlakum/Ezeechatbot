from pydantic import BaseModel


class UploadResponse(BaseModel):
    bot_id: str
    source_type: str
    chunks_stored: int
    message: str
