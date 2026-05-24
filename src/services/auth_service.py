from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from uuid import UUID


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "sua_chave_secreta_super_segura_para_o_chat_apple_2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7



class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(user_id: UUID,email: str) -> str:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": str(user_id),
            "email": email,
            "exp": expire 
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def verify_access_token(token: str) -> Optional[UUID]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id:str = payload.get("sub")
            if user_id is None:
                return None
            return UUID(user_id)
        except (jwt.PyJWTError, ValueError):
            return None


