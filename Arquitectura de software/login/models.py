from pydantic import BaseModel

# Esquema para recibir credenciales
class UserLogin(BaseModel):
    username: str
    password: str

# Esquema para la respuesta del token
class Token(BaseModel):
    access_token: str
    token_type: str
