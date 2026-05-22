from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    __tablename__: str = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    name: str = Field(max_length=100, nullable=False)
    email: str = Field(unique=True, max_length=255, nullable=False, index=True)
    password_hash: str = Field(nullable=False, max_length=255)
    avatar_url: Optional[str] = Field(default=None, nullable=True)

    is_online: bool = Field(default=False)
    last_seen_at: datetime = Field(default_factory=datetime.utcnow)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    chats_as_user_one: List["Chat"] = Relationship(
        sa_relationship_kwargs={"primaryjoin": "User.id == Chat.user_one_id"}

    )

    messages: List["Message"] = Relationship(back_populates="sender")

    