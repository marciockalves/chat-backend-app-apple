from sqlmodel import Session, select, and_,or_
from uuid import UUID
from datetime import datetime
from src.models.chat import Chats

class ChatService:
    @staticmethod
    async def get_or_create_private_chat(session: Session, user_id: UUID, recipient_id: UUID) -> Chats:
        
        u_id = UUID(str(user_id))
        r_id = UUID(str(recipient_id))
        
        statement = select(Chats).where(
            or_(
                and_(Chats.user_one_id == u_id, Chats.user_two_id == r_id),
                and_(Chats.user_one_id == r_id, Chats.user_two_id == u_id)
            )
        )
        result = await session.exec(statement)
        chat = result.first()
       
        if not chat:
            chat = Chats(
                user_one_id=user_id,
                user_two_id=recipient_id
            )
            session.add(chat)
            await session.commit()
            await session.refresh(chat)
            
        return chat
