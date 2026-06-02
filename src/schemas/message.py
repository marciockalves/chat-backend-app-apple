from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class MessageCreate(BaseModel):
    chat_id : UUID
    content: str

class MessageResponse(BaseModel):
    id: UUID
    chat_id: UUID
    content: str
    created_at: datetime

    class Config:
        from_attributes = True