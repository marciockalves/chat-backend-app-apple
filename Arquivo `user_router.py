from fastapi import APIRouter, Depends, HTTPException
from src.schemas import user
from src.services import auth_service
from src.config import database

router = APIRouter(prefix="/users")

@router.post("/register", response_model=user.UserCreate)
def register_user(user: user.UserCreate):
    db_user = User(username=user.username, email=user.email, password=auth_service.get_password_hash(user.password))
    database.session.add(db_user)
    database.session.commit()
    return db_user
