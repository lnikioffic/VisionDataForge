from typing import Tuple
from fastapi import HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from src.auth import utils as auth_utils


def get_authorization_scheme_param(
    authorization_header_value: str | None,
) -> Tuple[str, str]:
    if not authorization_header_value:
        return '', ''
    scheme, _, param = authorization_header_value.partition(' ')
    return scheme, param


class OAuthCustom(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> str | None:
        token = request.cookies.get('access_token')
        if not token:
            token = request.cookies.get('refresh_token')
        scheme, param = get_authorization_scheme_param(token)
        await self.assert_token(param)
        if not token or scheme.lower() != 'bearer':
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Not authenticated',
                    headers={'WWW-Authenticate': 'Bearer'},
                )
            else:
                return None
        return param

    async def assert_token(self, param: str):
        try:
            payload = auth_utils.decode_jwt(token=param)
        except InvalidTokenError as ex:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token',
                headers={'WWW-Authenticate': 'Bearer'},
            )
        return payload
