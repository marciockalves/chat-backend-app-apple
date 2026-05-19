from fastapi import APIRouter, WebSocket
from src.websocket import connection_manager

router = APIRouter(prefix="/ws")

@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You said: {data}", websocket)
            await manager.broadcast(f"Client says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
