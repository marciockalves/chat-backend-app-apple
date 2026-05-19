from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..config.database import SessionLocal
from ..schemas import UserOut
from ..services import auth_service

router = APIRouter(prefix="/users")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = auth_service.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
