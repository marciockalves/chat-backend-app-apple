from datetime import datetime
from typing import List
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship


class Chat(SQLModel, table=True):
    __tablename__: str = "chats"

    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    user_one_id: UUID = Field(nullable=False, foreign_key="users.id", ondelete="CASCADE")
    user_two_id: UUID = Field(nullable=False, foreign_key="users.id", ondelete="CASCADE")

    last_message_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    messages: List["Message"]= Relationship(
        back_populates="chat",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "order_by": "Message.created_at.desc()"}
    )

   