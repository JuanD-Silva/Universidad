from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from config import decode_access_token
from database import fake_users_db

# Esquema de seguridad para recibir el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Función para obtener usuario desde el token
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None or username not in fake_users_db:
        raise credentials_exception
    return fake_users_db[username]
