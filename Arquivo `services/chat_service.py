from sqlalchemy.orm import Session
from .models import Chat, Message
from .schemas import ChatCreate

def create_chat(db: Session, chat: ChatCreate):
    db_chat = Chat(user_id=chat.user_id, message=chat.message)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def get_chat(db: Session, chat_id: int):
    return db.query(Chat).filter(Chat.id == chat_id).first()
