# main.test.py

import os
from fastapi.testclient import TestClient
from src.main import app, lifespan
from src.config.settings import settings
from src.config.database import get_session, get_redis
from src.services.migrator_service import trigger_migration

os.environ["JWT_SECRET_KEY"] = "test_secret_key"
os.environ["POSTGRES_USER"] = "test_user"
os.environ["POSTGRES_PASSWORD"] = "test_password"
os.environ["POSTGRES_HOST"] = "localhost"
os.environ["POSTGRES_PORT"] = "5432"
os.environ["POSTGRES_DB"] = "test_db"

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(base_dir, ".env")
# load_dotenv(dotenv_path=dotenv_path)  # Descomente se precisar carregar o .env

client = TestClient(app)

async def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["project"] == settings.PROJECT_NAME
    assert data["message"] == "Backend do chat rodando com sucesso."

async def test_migrate_database():
    # Simulamos a migração da base de dados
    async with lifespan(app):
        pass  # Aqui você pode adicionar verificações adicionais se necessário

# Adicione mais testes conforme necessário para as rotas e funcionalidades do seu aplicativo