from fastapi import WebSocket
from typing import Dict, Optional
from uuid import UUID
import json


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[UUID, WebSocket] = {}

    async def connect(self, user_id: UUID, websocket: WebSocket, redis_client):

        await websocket.accept()
        self.active_connections[user_id] = websocket

        await redis_client.set(f"presence:{user_id}", "online")
        await redis_client.publish("presence", json.dumps({
            "user_id": str(user_id),
            "status": "online"
        }))
    async def disconnect(self, user_id: UUID, redis_client):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

        await redis_client.delete(f"presence:{user_id}")
        await redis_client.publish("presence_events", json.dumps({
            "user_id": str(user_id),
            "status": "offline" })
            )
    async def send_personal_message(self,  message: str, user_id: UUID):
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_json(message)

manager = ConnectionManager()