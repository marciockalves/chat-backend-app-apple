from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.config.database import get_session
from src.models.user import User
from src.schemas.auth import UserRegister, UserLogin, TokenResponse
from src.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
async def register(payload: UserRegister, db: AsyncSession= Depends(get_session)):
    query = select(User).where(User.email == payload.email)
    user = await db.execute(query)
    existing_use - result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")


    new_user = User(
        name=payload.name,
        email=payload.email,
        password_hash=AuthService.hash_password(payload.password)
       
         )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    token = AuthService.create_access_token(new_user.id, new_user.email)

    return TokenResponse(
        access_token=token,
        user_id=new_user.id,
        name=new_user.name,
    )

@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_session)):
    query = select(User).where(User.email == payload.email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if not user or not AuthService.verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = AuthService.create_access_token(user.id, user.email)

    return TokenResponse(
        access_token=token,
        user_id=user.id,
        name=user.name
    )
