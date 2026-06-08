import traceback
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import UUID
from typing import List

from src.config.database import get_session
from src.models.message import Message
from src.models.chat import Chats
from src.schemas.message import MessageCreate, MessageResponse
from src.dependencies.auth_dependency import get_current_user

router = APIRouter(prefix="/messages", tags=["Mensagens"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MessageResponse)
async def send_message(
    payload: MessageCreate,
    db: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    try:
        user_id = UUID(current_user["id"])

        chat_query = select(Chats).where(Chats.id==payload.chat_id)
        chat_result = await db.execute(chat_query)
        chat = chat_result.scalar_one_or_none()
                   
        if not chat:  # Adicione o caractere ":" aqui
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail= "Chat não encontrado."
            )
        new_message = Message(
            chat_id=payload.chat_id,
            sender_id=user_id,
            content=payload.content
        )

        db.add(new_message)
        await db.commit()
        await db.refresh(new_message)

        return new_message

    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print("\n"+"="*50)
        print(f"=== ERRO AO ENVIAR MENSAGEM: {str(e)} ===")
        traceback.print_exc()
        print("="*50+"\n")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao enviar mensagem"
        )

    @router.get("/{chat_id}/messages", response_model=List[MessageResponse])
    async def get_chat_messages(chat_id: int, db: AsyncSession = Depends(get_session), current_user: dict = Depends(get_current_user)):
        try:
            chat_query = select(Chat).where(Chat.id == chat_id)
            chat_result = await db.execute(chat_query)
            chat = chat_result.scalar_one_or_none()
            if not chat:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail ="Chat não encontrado"
                
                )

            query = (
                select(Message).
                where(Message.chat_id == chat.id).
                order_by(Message.created_at.asc())
            )

            result = await db.execute(query)
            messages = result.scalars().all()
            return messages
        except HTTPException as http_err:
            raise http_err
        except Exception as e:
            print("\n" + "=="*50)
            print(f"===EWRRO AO BUSCAR HISTÓRICO: {str(e)} ====")
            traceback.print_exc()
            print("=="*50 + "\n")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER,
                detail="Erro ao buscar histórico de mensagens"
            )