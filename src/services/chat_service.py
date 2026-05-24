from sqlmodel import Session, select, and_,or_
from uuid import UUID
from datetime import datetime
from src.models.chat import Chats

class ChatService:
    @staticmethod
    def get_or_create_private_chat(session: Session, user_id: UUID, recipient_id: UUID) -> Chats:
        
        statement = select(Chats).where(
            or_(
                and_(Chats.creator_id == user_id, Chats.recipient_id == recipient_id),
                and_(Chats.creator_id = recipient_id, Chats.recipient_id == user_id)
            )
        )
        existing_chat = session.exec(statement).first()

        if existing_chat:
            return existing_chat

        
        new_chat= Chats(
            creator_id = user_id,
            recipient_id=recipient_id,
            created_at=datetime.utcnow(),
            last_message_at=datetime.utcnow()
        )
        session.add(new_chat)
        session.commit()
        session.refresh(new_chat)
        return new_chat
