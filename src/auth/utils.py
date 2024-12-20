from fastapi import Request
import jwt
import bcrypt
from datetime import timedelta, datetime
from src.auth.config import auth_jwt


def encode_jwt(
    payload: dict,
    private_key: str = auth_jwt.private_key_path.read_text(),
    algorithm: str = auth_jwt.algorithm,
    expire_timedelta: timedelta | None = None,
    expire_minutes: int = auth_jwt.access_token_expire_minutes,
):
    to_encode = payload.copy()
    now = datetime.utcnow()

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        iat=now,
        exp=expire,
    )
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = auth_jwt.public_key_path.read_text(),
    algorithm: str = auth_jwt.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hash_password: str) -> bool:
    return bcrypt.checkpw(
        password=password.encode(), hashed_password=hash_password.encode()
    )


async def get_cookies_for_login_registration(request: Request) -> bool:
    token = request.cookies.get('access_token')
    if not token:
        token = request.cookies.get('refresh_token')
        
    if token:
        return True
    return False