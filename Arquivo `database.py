from sqlmodel import SQLModel, create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

def get_session():
    from sqlmodel import Session
    session = Session(bind=engine)
    try:
        yield session
    finally:
        session.close()
