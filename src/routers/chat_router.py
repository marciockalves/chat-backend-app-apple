from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from src.schemas.chat import ChatCreate
from src.services.chat_service import ChatService
from src.config.database import get_session
from src.dependencies.auth_dependency import get_current_user
from uuid import UUID
import traceback

router = APIRouter(prefix="/chats", tags=["Chats"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_chat(
    payload: ChatCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user)
    ):
    try:
        user_id_raw = current_user.get("id") or current_user.get("sub")
        if not user_id_raw:
            raise HTTPException(status_code=401, detail="ID de usuário não encontrado.")
        user_id = UUID(str(user_id_raw))
        if user_id == payload.recipient_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Você não pode criar um chat com você mesmo.")

        chat = await ChatService.get_or_create_private_chat(
            session=session,
            user_id=user_id,
            recipient_id=payload.recipient_id
        )
        return chat
    
    except HTTPException as e:
        raise e
    
    except Exception as e:
        print("\n" + "="*50)
        print(f"=== ERRO REAL NO CHAT ROUTER: {str(e)} ===")
        traceback.print_exc()
        print("="*50 + "\n")
        raise HTTPException(status_code=500, detail=str(e))
