import os
from dotenv import load_dotenv

load_dotenv()

# Configurações do projeto
PROJECT_NAME = "meu-chat-backend"
API_V1_STR = "/api/v1"

# Configurações de banco de dados
DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:///./test.db"
