from datetime import timedelta

from src.users.schemas import UserRead
from src.auth import utils as auth_utils
from src.auth.config import auth_jwt


TOKEN_TYPE_FIELD = 'type'
ACCESS_TOKEN_TYPE = 'access'
REFRESH_TOKEN_TYPE = 'refresh'


async def create_token(
    token_type: str,
    payload: dict,
    expire_minutes: int = auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:

    jwt_payload = {TOKEN_TYPE_FIELD: token_type}

    jwt_payload.update(payload)

    return auth_utils.encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


async def create_access_token(user: UserRead) -> str:
    payload = {
        'sub': str(user.id),
        'user': {
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active,
            'is_superuser': user.is_superuser,
        },
    }

    token = 'Bearer ' + await create_token(
        token_type=ACCESS_TOKEN_TYPE,
        payload=payload,
        expire_minutes=auth_jwt.access_token_expire_minutes,
    )
    return token


async def create_refresh_token(user: UserRead) -> str:
    payload = {
        'sub': str(user.id),
    }

    token = 'Bearer ' + await create_token(
        token_type=REFRESH_TOKEN_TYPE,
        payload=payload,
        expire_timedelta=timedelta(days=auth_jwt.refresh_token_expire_days),
    )
    return token
