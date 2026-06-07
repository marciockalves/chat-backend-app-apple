# src/tests/test_auth_router.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSessionLocal

from src.config.database import get_session, engine
from src.main import app
from src.models.user import User
from src.schemas.auth import UserRegister, TokenResponse
from src.services.auth_service import AuthService


# Configuração do banco de dados para testes
DATABASE_URL_TEST = "sqlite+aiosqlite:///./test.db"

engine_test = create_async_engine(DATABASE_URL_TEST, echo=True)
async_session_local_test = AsyncSessionLocal(bind=engine_test)

app.dependency_overrides[get_session] = async_session_local_test

# Função para criar o banco de dados e as tabelas
@pytest.fixture(scope="module")
async def init_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


# Função para criar um cliente de teste
@pytest.fixture(scope="module")
async def client(init_db):
    async with TestClient(app) as client:
        yield client


# Teste para a rota de registro
@pytest.mark.asyncio
async def test_register(client):
    payload = UserRegister(
        name="Test User",
        email="test@example.com",
        password="password123"
    )

    response = await client.post("/auth/register", json=payload.dict())
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "user_id" in data
    assert "name" in data


# Teste para a rota de login com credenciais válidas
@pytest.mark.asyncio
async def test_login_success(client):
    payload_register = UserRegister(
        name="Test User",
        email="test@example.com",
        password="password123"
    )
    response_register = await client.post("/auth/register", json=payload_register.dict())
    assert response_register.status_code == 201

    payload_login = UserLogin(
        email="test@example.com",
        password="password123"
    )
    response_login = await client.post("/auth/login", json=payload_login.dict())
    assert response_login.status_code == 200
    data = response_login.json()
    assert "access_token" in data


# Teste para a rota de login com credenciais inválidas
@pytest.mark.asyncio
async def test_login_failure(client):
    payload_login = UserLogin(
        email="test@example.com",
        password="wrongpassword"
    )
    response_login = await client.post("/auth/login", json=payload_login.dict())
    assert response_login.status_code == 401