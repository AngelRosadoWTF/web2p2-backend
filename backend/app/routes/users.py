from fastapi import APIRouter, Depends, HTTPException, Request
from jose import jwt, JWTError
from sqlmodel import Session, select
from app.database.conexion import getSession
from app.database.models import User
from app.config import SECRET_KEY, ALGORITHM

router = APIRouter()

@router.get("/users/me")
def get_current_user(
    request: Request,
    session: Session = Depends(getSession)
):
    token = None
    auth_header = request.headers.get("Authorization")

    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]

    if not token:
        token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(
            status_code=401,
            detail="No autorizado"
        )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if not username:
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    user = session.exec(
        select(User).where(User.username == username)
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return user