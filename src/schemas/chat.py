from pydantic import BaseModel
from uuid import UUID

class ChatCreate(BaseModel):
    recipient_id: UUID