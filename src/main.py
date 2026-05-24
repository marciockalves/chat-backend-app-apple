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

from src.models import User, Chat, Message

from src.routers.auth_router import router as auth_router
from src.websocket.ws_router import router as ws_router

from dotenv import load_dotenv


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(base_dir, ".env")
load_dotenv(dotenv_path=dotenv_path)


def run_auto_migration():
    """Função síncrona que executa os comandos do Alembic"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ini_path = os.path.join(base_dir, "alembic.ini")
    
    cfg = Config(ini_path)
    cfg.set_main_option("script_location", os.path.join(base_dir, "alembic"))
    
    # Tenta buscar pelas chaves mais comuns de banco de dados
    db_url = os.getenv("DATABASE_URL") or os.getenv("DB_URL") or os.getenv("POSTGRES_URL")
    
    if db_url:
        print(f"=== [Alembic] URL detectada com sucesso! ===")
        if "postgresql+asyncpg://" in db_url:
            db_url = db_url.replace("postgresql+asyncpg://", "postgresql://")
        
        cfg.set_main_option("sqlalchemy.url", db_url)
    else:
        print("=== [Alembic] ERRO CRÍTICO: Nenhuma variável de banco encontrada no .env ===")
        # Mostra o que tem no seu .env para ajudar a diagnosticar o nome da chave
        print(f"Chaves disponíveis no ambiente: {list(os.environ.keys())}")
    
    print("=== [Alembic] Verificando alterações nos modelos ===")
    try:
        command.revision(cfg, message="auto_migration", autogenerate=True)
        print("=== [Alembic] Nova versão de migration gerada ===")
    except Exception as e:
        print(f"=== [Alembic] Sem alterações pendentes para gerar: {e} ===")

    print("=== [Alembic] Aplicando migrations pendentes (upgrade head) ===")
    try:
        command.upgrade(cfg, "head")
        print("=== [Alembic] Banco de dados atualizado com sucesso! ===")
    except Exception as e:
        print(f"=== [Alembic] Erro ao aplicar upgrade: {e} ===")


async def trigger_migration():
    """Roda a migração em uma thread separada para não bloquear o FastAPI"""
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, run_auto_migration)


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    app.state.redis = get_redis()
    print("=== Conexão com Redis estabelecida com sucesso ===")
    await trigger_migration()
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