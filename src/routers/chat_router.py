from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from src.schemas.chat import ChatCreate
from src.services.chat_service import ChatService
from src.config.database import get_session
from src.dependencies.auth_dependency import get_current_user

router = APIRouter(prefix="/chats", tags=["Chats"])


@router.post("/", response_model=ChatCreate)
async def create_chat(
    payload: ChatCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
    ):
    user_id= current_user.get("id")

    if user_id == payload.recipient_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Você não pode criar um chat com você mesmo.")

    chat = ChatService.get_or_create_private_chat(
        session=session,
        user_id=user_id,
        recipient_id=payload.recipient_id
    )
    return chat

