from passlib.context import CryptContext
from src.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    user = User.query.filter(User.username == username).first()
    if not user or not verify_password(password, user.password):
        return False
    return user
