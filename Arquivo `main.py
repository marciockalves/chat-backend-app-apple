from fastapi import FastAPI
from src.routers import auth_router, user_router, chat_router
from src.websocket import connection_manager, ws_router

app = FastAPI()

# Incluir rotas
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(chat_router.router)
app.include_router(ws_router.router, prefix="/ws")

# Gerenciador de conexões WebSocket
app.websocket("/ws")(connection_manager.WebSocketManager())
