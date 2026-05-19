from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..config.database import SessionLocal
from ..schemas import ChatCreate, ChatOut
from ..services import chat_service

router = APIRouter(prefix="/chats")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ChatOut)
def create_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    return chat_service.create_chat(db, chat)

@router.get("/{chat_id}", response_model=ChatOut)
def read_chat(chat_id: int, db: Session = Depends(get_db)):
    chat = chat_service.get_chat(db, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat
