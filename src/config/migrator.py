import os
from alembic import command
from alembic.config import Config
import asyncio

def run_auto_migration():
    # Carrega o arquivo alembic.ini da raiz do projeto
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    ini_path = os.path.join(base_dir, "alembic.ini")
    
    cfg = Config(ini_path)
    
    # Garante que o Alembic aponte para a pasta correta de migrations
    cfg.set_main_option("script_location", os.path.join(base_dir, "alembic"))
    
    print("=== [Migrator] Verificando alterações nos modelos ===")
    
    try:
        # 1. Tenta gerar a migration automaticamente detectando mudanças
        # Se não houver mudanças, o Alembic pode lançar uma exceção ou gerar vazia
        command.revision(cfg, message="auto_migration", autogenerate=True)
        print("=== [Migrator] Nova migration gerada com sucesso ===")
    except Exception as e:
        # O Alembic falha ou avisa se não houver o que alterar
        print(f"=== [Migrator] Nenhuma alteração pendente ou erro na geração: {e} ===")

    print("=== [Migrator] Aplicando migrations pendentes (upgrade head) ===")
    # 2. Aplica as migrations de qualquer forma para garantir o banco atualizado
    command.upgrade(cfg, "head")
    print("=== [Migrator] Banco de dados atualizado! ===")

async def trigger_migration():
    # Como o Alembic síncrono bloqueia o loop assíncrono do FastAPI,
    # rodamos ele dentro de um executor para não travar a API no startup.
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, run_auto_migration)