from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd = CryptContext(schemes=["argon2"], deprecated="auto")

def pwdHash(password: str):
    return pwd.hash(password)

def pwdVerify(plain_password: str, hashed_password: str):
    return pwd.verify(plain_password, hashed_password)

def crearToken(data: dict):
    to_encode = data.copy()
    expire = datetime + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt