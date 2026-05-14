from pydantic import BaseModel

class CrearUsuario(BaseModel):
    full_name: str
    username: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class UsuarioResponse(BaseModel):
    id: int
    full_name: str
    username: str
    hashed_password: str