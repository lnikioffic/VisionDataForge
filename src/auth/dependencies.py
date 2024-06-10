from typing import Annotated
from fastapi import Depends, HTTPException, status, Form
from jwt.exceptions import InvalidTokenError

from src.auth.oauth import OAuthCustom
from src.auth.token import (
    create_access_token,
    create_refresh_token,
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
)
from src.users.dependencies import valid_user_id, valid_user_username
from src.users.schemas import UserRead
from src.auth.schemas import TokenInfo, AuthForm
from src.auth import utils as auth_utils
from src.users.service import UserService


oauth = OAuthCustom(tokenUrl='/auth/token')


async def get_current_token_payload(token: Annotated[str, Depends(oauth)]) -> UserRead:
    try:
        payload = auth_utils.decode_jwt(token=token)
    except InvalidTokenError as ex:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return payload


async def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f'invalid token type {current_token_type!r} expected {token_type!r}',
    )


async def get_user_by_token_sub(
    payload: Annotated[dict, Depends(get_current_token_payload)],
    service: Annotated[UserService, Depends()],
) -> UserRead:
    id: str | None = payload.get('sub')
    if user := await valid_user_id(int(id), service):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='token invalid (user not found)',
    )


async def get_current_auth_user(
    payload: Annotated[dict, Depends(get_current_token_payload)],
    service: Annotated[UserService, Depends()],
) -> UserRead:
    await validate_token_type(payload=payload, token_type=ACCESS_TOKEN_TYPE)
    id: str | None = payload.get('sub')
    if user := await valid_user_id(int(id), service):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='token invalid (user not found)',
    )


async def get_current_auth_user_for_refresh(
    payload: Annotated[dict, Depends(get_current_token_payload)],
    service: Annotated[UserService, Depends()],
) -> UserRead:
    await validate_token_type(payload=payload, token_type=REFRESH_TOKEN_TYPE)
    id: str | None = payload.get('sub')
    if user := await valid_user_id(int(id), service):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='token invalid (user not found)',
    )


async def get_current_active_auth_user(
    user: Annotated[UserRead, Depends(get_current_auth_user)]
) -> UserRead:

    if user.is_active:
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='user inactive',
    )


async def validate_auth_user(
    # data_form: Annotated[AuthForm, Depends()],
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    service: Annotated[UserService, Depends()],
) -> TokenInfo:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='invalid username or password',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    user: UserRead = await valid_user_username(username, service)
    if not user:
        raise unauthed_exc

    if not auth_utils.validate_password(
        password=password,
        hash_password=user.hashed_password,
    ):
        raise unauthed_exc

    return await create_token_jwt(user)


async def validate_create_user(
    user: UserRead,
) -> TokenInfo:

    return await create_token_jwt(user)


async def create_token_jwt(user: UserRead) -> TokenInfo:
    access_token = await create_access_token(user)
    refresh_token = await create_refresh_token(user)

    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


async def refresh_token_jwt(user: UserRead) -> TokenInfo:
    access_token = await create_access_token(user)

    return TokenInfo(access_token=access_token)


async def delete_token_jwt(user: UserRead) -> TokenInfo:

    return TokenInfo(access_token='', refresh_token=None)
