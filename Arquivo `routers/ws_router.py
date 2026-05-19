from fastapi import APIRouter, WebSocket
from ..websocket import connection_manager

router = APIRouter(prefix="/ws")

@router.websocket("/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await connection_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await connection_manager.send_personal_message(data, client_id)
    except Exception as e:
        print(f"Error: {e}")
        await connection_manager.disconnect(websocket)
