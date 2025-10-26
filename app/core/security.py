from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def safe_password(password: str) -> str:
    pw_bytes = password.encode("utf-8")
    truncated = pw_bytes[:72]
    return truncated.decode("utf-8", errors="ignore")


def hash_password(password: str) -> str:
    return pwd_context.hash(safe_password(password))


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(safe_password(plain), hashed)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
