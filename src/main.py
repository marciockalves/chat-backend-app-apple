from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.settings import settings
from src.config.database import get_session, get_redis
from src.models import User, Chat, Message


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    app.state.redis = get_redis()
    print("=== Conexão com Redis estabelecida com sucesso ===")
    
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


@app.get("/")
async def root():
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "message": "Backend do chat rodando com sucesso."
    }