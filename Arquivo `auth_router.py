from fastapi import APIRouter, Depends, HTTPException
from src.schemas import auth, user
from src.services import auth_service
from src.config import database

router = APIRouter(prefix="/auth")

@router.post("/login", response_model=auth.Token)
def login(login: auth.AuthLogin):
    user = auth_service.authenticate_user(login.username, login.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
