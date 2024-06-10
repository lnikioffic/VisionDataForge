from typing import Annotated
import asyncio
from fastapi import APIRouter, Form, Request, Depends, Response, HTTPException, status
from fastapi.datastructures import Headers
from fastapi.security import HTTPBearer

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse

from src.users.schemas import UserCreate, UserRead
from src.auth.schemas import TokenInfo
from src.auth.dependencies import (
    validate_auth_user,
    get_current_active_auth_user,
    get_current_token_payload,
    refresh_token_jwt,
    delete_token_jwt,
    get_current_auth_user_for_refresh,
    validate_create_user,
)

from src.users.service import UserService

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(prefix='/auth', tags=['Auth'], dependencies=[Depends(http_bearer)])

router.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')


# Отображает раздел для авторизации пользователя
@router.get('/login', response_class=HTMLResponse)
async def get_user_login(
    request: Request, user: Annotated[UserRead, Depends(get_current_active_auth_user)]
):
    if not user:
        return templates.TemplateResponse(request=request, name='user-login-get.html')
    return RedirectResponse(url='/users/profile')


# Отображает раздел для регистрации пользователя
@router.get('/registration', response_class=HTMLResponse)
async def get_user_registration(
    request: Request, user: Annotated[UserRead, Depends(get_current_active_auth_user)]
):
    if not user:
        return templates.TemplateResponse(
            request=request, name='user-registration-get.html'
        )
    return RedirectResponse(url='/users/profile')


# Отображает раздел для восстановления пароля пользователя
@router.get('/password-put', response_class=HTMLResponse)
async def put_user_password(request: Request):
    return templates.TemplateResponse(request=request, name='user-password-put.html')


@router.post('/create', response_model=TokenInfo)
async def sing_up(
    response: Response, user: UserCreate, service: Annotated[UserService, Depends()]
):
    res = await service.create_user(user)
    token = await validate_create_user(res)
    response.set_cookie(
        key='access_token',
        value=token.access_token,
        secure=True,
        httponly=True,
        max_age=3600,
    )
    response.set_cookie(
        key='refresh_token',
        value=token.refresh_token,
        secure=True,
        httponly=True,
        max_age=604800,
    )
    return token


@router.post('/token', response_model=TokenInfo)
async def auth(response: Response, token: Annotated[str, Depends(validate_auth_user)]):
    response.set_cookie(
        key='access_token',
        value=token.access_token,
        secure=True,
        httponly=True,
        max_age=3600,
    )
    response.set_cookie(
        key='refresh_token',
        value=token.refresh_token,
        secure=True,
        httponly=True,
        max_age=604800,
    )
    return token


@router.api_route(
    '/refresh',
    methods=['POST', 'GET'],
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
async def auth_refresh_jwt(
    request: Request,
    user: Annotated[UserRead, Depends(get_current_auth_user_for_refresh)],
    redirect_url: str = None,
):
    token = await refresh_token_jwt(user)
    redirect_url = request.cookies.get('current_url')
    if redirect_url:
        # Создание RedirectResponse
        redirect_response = RedirectResponse(redirect_url)
        # Копирование установленных куки в RedirectResponse
        redirect_response.set_cookie(
            key='access_token',
            value=token.access_token,
            secure=True,
            httponly=True,
            max_age=3600,
        )
        redirect_response.delete_cookie(key='current_url')
        # Возвращение RedirectResponse
        return redirect_response
    else:
        # Если заголовок Referer не найден, возвращаем новый токен доступа
        return token


@router.post('/logout', response_model=TokenInfo, response_model_exclude_none=True)
async def logout(
    response: Response, user: Annotated[UserRead, Depends(get_current_active_auth_user)]
):
    token = await delete_token_jwt(user)
    response.delete_cookie(key='access_token')
    response.delete_cookie(key='refresh_token')
    return token
