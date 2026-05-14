from sqlmodel import Session, select
from app.database.models import User
from app.services.security import pwdHash, pwdVerify

DUMMY_HASH = pwdHash("dummy_password")

def crearUsuario(session: Session, full_name: str, username: str, password: str):
    existing_user = session.exec(
        select(User).where(User.username == username)
    ).first()

    if existing_user:
        return None

    user = User(
        full_name=full_name,
        username=username,
        hashed_password=pwdHash(password)
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def autenticarUsuario(session: Session, username: str, password: str):
    user = session.exec(
        select(User).where(User.username == username)
    ).first()

    if not user:
        pwdVerify(password, DUMMY_HASH)
        return None

    if not pwdVerify(password, user.hashed_password):
        return None

    return user