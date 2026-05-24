import os
import asyncio
from alembic import command
from alembic.config import Config

def _writer(context, revision, directives):
    """Callback interno do Alembic para evitar arquivos de migration vazios"""
    if directives:
        script = directives[0]
        if script.upgrade_ops.is_empty():
            directives[:] = []
            print("=== [Alembic] Nenhuma mudança estrutural detectada. Arquivo cancelado. ===")

def run_auto_migration(db_credentials: dict):
    """Executa os comandos do Alembic usando as credenciais injetadas"""
    # Encontra a raiz do projeto para localizar o alembic.ini
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ini_path = os.path.join(base_dir, "alembic.ini")
    
    cfg = Config(ini_path)
    cfg.set_main_option("script_location", os.path.join(base_dir, "alembic"))
    
    user = db_credentials.get("POSTGRES_USER")
    password = db_credentials.get("POSTGRES_PASSWORD")
    host = db_credentials.get("POSTGRES_HOST")
    port = db_credentials.get("POSTGRES_PORT")
    db = db_credentials.get("POSTGRES_DB")
    
    if not all([user, password, host, port, db]):
        print("=== [Alembic] ERRO CRÍTICO: Credenciais injetadas estão incompletas ===")
        return

    # Monta a URL síncrona perfeitamente
    db_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    cfg.set_main_option("sqlalchemy.url", db_url)
    
    print("=== [Alembic] Verificando alterações nos modelos ===")
    try:
        command.revision(
            cfg, 
            message="auto_migration", 
            autogenerate=True, 
            process_revision_directives=_writer
        )
    except Exception as e:
        print(f"=== [Alembic] Erro ou aviso na checagem: {e} ===")

    print("=== [Alembic] Aplicando migrations pendentes (upgrade head) ===")
    try:
        command.upgrade(cfg, "head")
        print("=== [Alembic] Banco de dados atualizado com sucesso! ===")
    except Exception as e:
        print(f"=== [Alembic] Erro ao aplicar upgrade: {e} ===")

async def trigger_migration(db_credentials: dict):
    """Desvia a execução síncrona injetando os parâmetros no executor"""
    loop = asyncio.get_running_loop()
    # Passamos db_credentials como argumento para a thread secundária rodar de forma segura
    await loop.run_in_executor(None, run_auto_migration, db_credentials)