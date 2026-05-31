from datetime import datetime, timedelta
import os  # <-- Adicionado para ler o .env
from typing import Optional
from jose import jwt, JWTError  # <-- Mudado de 'import jwt' para 'jose'
from passlib.context import CryptContext
from uuid import UUID

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    def create_access_token(user_id: UUID, email: str) -> str:
        # Pega a chave real do .env no momento de gerar o token
        secret_key = os.getenv("JWT_SECRET_KEY")
        
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload = {
            "sub": str(user_id),
            "email": email,
            "exp": expire 
        }
        # Nota: python-jose usa 'algorithm' no singular aqui
        return jwt.encode(payload, secret_key, algorithm=ALGORITHM)
    
    @staticmethod
    def verify_access_token(token: str) -> Optional[UUID]:
        try:
            secret_key = os.getenv("JWT_SECRET_KEY")
            payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            return UUID(user_id)
        except (JWTError, ValueError):  # <-- Mudado para capturar o erro da jose
            return None