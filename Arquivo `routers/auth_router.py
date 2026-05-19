from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..config.database import SessionLocal
from ..schemas import UserCreate, UserLogin, UserOut
from ..services import auth_service

router = APIRouter(prefix="/auth")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return auth_service.create_user(db, user)

@router.post("/login", response_model=UserOut)
def login(user: UserLogin, db: Session = Depends(get_db)):
    authenticated_user = auth_service.authenticate_user(db, user)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return authenticated_user
