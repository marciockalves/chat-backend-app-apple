from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field, Relationship


class MessageType(str, Enum):
    TEXT= "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    CALL_LOG = "call_log"


class Message(SQLModel, table=True):
    __tablename__: str = "message"

    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    chat_id: UUID = Field(nullable=False, foreign_key="chats.id", ondelete="CASCADE")
    sender_id: UUID = Field(nullable=False, foreign_key="users.id", ondelete="CASCADE")
    type: MessageType = Field(default=MessageType.TEXT, nullable=True)
    content: Optional[str] = Field(default=None, nullable=True)
    file_url: Optional[str] = Field(default=None, nullable=True)
    file_metadata: Optional[dict]= Field(
        default=None,
        sa_column=Column(JSONB, nullable=True)
    )

    is_delivered: bool = Field(default=False)
    is_read: bool = Field(default=False)

    delivered_at: Optional[datetime]= Field(default=None, nullable=True)
    read_at: Optional[datetime] = Field(default=None,nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    chat: Optional["Chats"] = Relationship(back_populates="messages")
    sender: Optional["User"]= Relationship(back_populates="messages")