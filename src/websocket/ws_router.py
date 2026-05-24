from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from sqlmodel import select
import json
from uuid import UUID

from src.config.database import async_session_maker, get_redis
from src.services.auth_service import AuthService
from src.websocket.connection_manager import manager
from src.models.message import Message, MessageType
from src.models.chat import Chat

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...)
):
   
    user_id = AuthService.verify_access_token(token)
    if not user_id:
        await websocket.close(code=4003)  
        return

    redis_client = get_redis()
    await manager.connect(user_id, websocket, redis_client)

    try:
        while True:
            raw_data = await websocket.receive_text()
            data = json.loads(raw_data)
            
            chat_id = UUID(data["chat_id"])
            receiver_id = UUID(data["receiver_id"])
            content = data["content"]

         
            async with async_session_maker() as db:
                new_message = Message(
                    chat_id=chat_id,
                    sender_id=user_id,
                    type=MessageType.TEXT,
                    content=content,
                    is_delivered=False
                )
                db.add(new_message)
            
                query_chat = select(Chat).where(Chat.id == chat_id)
                chat_result = await db.execute(query_chat)
                chat = chat_result.scalar_one_or_none()
                if chat:
                    chat.last_message_at = new_message.created_at
                    db.add(chat)

                await db.commit()
                await db.refresh(new_message)
                
              
                created_at_iso = new_message.created_at.isoformat()

          
            message_payload = {
                "id": str(new_message.id),
                "chat_id": str(chat_id),
                "sender_id": str(user_id),
                "type": "text",
                "content": content,
                "created_at": created_at_iso
            }

           
            await manager.send_personal_message(message_payload, user_id)
            await manager.send_personal_message(message_payload, receiver_id)

    except WebSocketDisconnect:
        await manager.disconnect(user_id, redis_client)
    finally:
        await redis_client.close()