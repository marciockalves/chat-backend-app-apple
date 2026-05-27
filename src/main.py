import os
import asyncio

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from alembic import command
from alembic.config import Config


from src.config.settings import settings
from src.config.database import get_session, get_redis
from src.config.migrator import trigger_migration

from src.models import User, Chats, Message

from src.routers.auth_router import router as auth_router
from src.websocket.ws_router import router as ws_router
from src.routers.chat_router import router as chat_router


from dotenv import load_dotenv


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(base_dir, ".env")
load_dotenv(dotenv_path=dotenv_path)

from src.config.database import get_redis 
from src.services.migrator_service import trigger_migration


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    app.state.redis = get_redis()
    print("=== Conexão com Redis estabelecida com sucesso ===")
    credentials = {
        "POSTGRES_USER": os.getenv("POSTGRES_USER"),
        "POSTGRES_PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "POSTGRES_HOST": os.getenv("POSTGRES_HOST"),
        "POSTGRES_PORT": os.getenv("POSTGRES_PORT"),
        "POSTGRES_DB": os.getenv("POSTGRES_DB"),
    }
    await trigger_migration(db_credentials=credentials)
    yield
    
    await app.state.redis.close()
    print("=== Conexão com Redis encerrada de forma limpa ===")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para o chat",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # No futuro, restringir para os domínios do app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(ws_router)

@app.get("/")
async def root():
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "message": "Backend do chat rodando com sucesso."
    }