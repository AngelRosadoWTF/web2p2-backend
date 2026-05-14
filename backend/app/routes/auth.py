from fastapi import APIRouter, Depends, HTTPException, Response, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.database.conexion import getSession
from app.schemas.schema import CrearUsuario
from app.services.auth_service import crearUsuario, autenticarUsuario
from app.services.security import crearToken

router = APIRouter()

@router.post("/register")
def register_user(
    user_data: CrearUsuario,
    session: Session = Depends(getSession)
):
    user = crearUsuario(
        session,
        user_data.full_name,
        user_data.username,
        user_data.password
    )

    if not user:
        raise HTTPException(
            status_code=400,
            detail="El usuario ya existe"
        )

    return {
        "message": "Usuario creado correctamente"
    }

@router.post("/login/cookie")
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(getSession)
):
    user = autenticarUsuario(
        session,
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    token = crearToken(
        {"sub": user.username}
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=180,
        expires=180,
        samesite="lax"
    )

    return{
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/login/header")
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(getSession)
):
    user = autenticarUsuario(
        session,
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )

    token = crearToken(
        {"sub": user.username}
    )

    response.headers["Token"] = token

    return{
        "access_token": token,
        "token_type": "bearer"
    }