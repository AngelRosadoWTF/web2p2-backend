from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

pwd = CryptContext(schemes=["argon2"], deprecated="auto")

def pwdHash(password: str):
    return pwd.hash(password)

def pwdVerify(plain_pwd: str, hashed_pwd: str):
    return pwd.verify(plain_pwd, hashed_pwd)

def crearToken(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt