from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

async def get_current_user(token: str= Depends(oauth2_scheme)) -> dict:

        

        try:
            print("\n" + "•"*50)
            print(f"=== DEBUGA_TOKEN: Recebeu o token do Postman: {token[:20]}... ===")

            credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autenticação inválido",
            headers={"WWW-Authenticate": "Bearer"}
            )
            payload= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            print(f"=== DEBUGA_TOKEN: Payload decodificado com sucesso: {payload} ===")
            user_id: str = payload.get("sub")
            email: str = payload.get("email")
            name: str = payload.get("name")

            print(f"=== DEBUGA_TOKEN: Dados extraídos -> user_id: {user_id}, email: {email} ===")

            if user_id is None or email is None:
                print("=== DEBUGA_TOKEN: user_id veio nulo! Lançando 401 ===")
                raise credentials_exception

            return {
                "id": user_id,
                "email": email,
                "name": name
            }

        except JWTError as jwt_err:
            print(f"=== DEBUGA_TOKEN: Falha na biblioteca JWT (jose): {str(jwt_err)} ===")
            raise credentials_exception
        except Exception as e:
            print("\n" + "="*50)
            print(f"=== BUG ENCONTRADO NO GET_CURRENT_USER: {str(e)} ===")
            traceback.print_exc()
            print("="*50 + "\n")
            raise HTTPException(status_code=500, detail=f"Erro interno na validação do token: {str(e)}")