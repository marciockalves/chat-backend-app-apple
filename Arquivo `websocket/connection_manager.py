from fastapi import WebSocket
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, client_id: str):
        for connection in self.active_connections:
            if connection.client == client_id:
                await connection.send_text(message)
