# Variáveis reutilizáveis
PYTHON_MODULE = src.main:app
COMPOSE_CMD = podman compose

.PHONY: help up down restart ps logs backend-dev uv-sync uv-clean db-upgrade db-migrate

# Comando padrão (se você digitar apenas 'make' no terminal)
help:
	@echo "=== Comandos Disponíveis no Projeto ==="
	@echo "--- Infraestrutura (Podman) ---"
	@echo "  make up          - Sobe os containers (Postgres, Redis, DbGate) em segundo plano"
	@echo "  make down        - Derruba os containers e mantém os volumes"
	@echo "  make restart     - Reinicia os containers"
	@echo "  make ps          - Lista os containers ativos"
	@echo "  make logs        - Mostra e acompanha os logs dos containers"
	@echo ""
	@echo "--- Aplicação & Pacotes (UV) ---"
	@echo "  make run         - Executa o servidor backend FastAPI em modo desenvolvimento"
	@echo "  make sync        - Sincroniza e atualiza os pacotes com base no pyproject.toml"
	@echo "  make clean       - Remove o ambiente virtual (.venv) e arquivos de cache"
	@echo ""
	@echo "--- Banco de Dados (Alembic Migrations) ---"
	@echo "  make db-migrate m='mensagem' - Cria uma nova versão de migração do banco"
	@echo "  make db-upgrade              - Aplica as migrações pendentes no banco de dados"

# --- INFRAESTRUTURA ---
up:
	$(COMPOSE_CMD) up -d

down:
	$(COMPOSE_CMD) down

restart:
	$(COMPOSE_CMD) restart

ps:
	$(COMPOSE_CMD) ps

logs:
	$(COMPOSE_CMD) logs -f

# --- APLICAÇÃO & PACOTES ---
run:
	uv run uvicorn $(PYTHON_MODULE) --reload --host 0.0.0.0 --port 8000

sync:
	uv sync

clean:
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +

# --- BANCO DE DADOS ---
db-migrate:
	uv run alembic revision --autogenerate -m "$(m)"

db-upgrade:
	uv run alembic upgrade head