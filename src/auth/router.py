from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.security import HTTPBearer

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from src.users.schemas import UserCreate, UserRead
from src.auth.schemas import TokenInfo
from src.auth.dependencies import (
    validate_auth_user, 
    get_current_active_auth_user, 
    get_current_token_payload,
    refresh_token_jwt,
    get_current_auth_user_for_refresh,
    validate_create_user
)

from src.users.service import ServiceUser

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(prefix='/auth', tags=['Auth'], dependencies=[Depends(http_bearer)])

router.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory="templates")


#Отображает раздел для авторизации пользователя
@router.get("/login", response_class=HTMLResponse)
async def get_user_login(request: Request):
    return templates.TemplateResponse(request=request, name="user-login-get.html")


#Отображает раздел для регистрации пользователя
@router.get("/registration", response_class=HTMLResponse)
async def get_user_registration(request: Request):
    return templates.TemplateResponse(request=request, name="user-registration-get.html")


#Отображает раздел для восстановления пароля пользователя
@router.get("/password-put", response_class=HTMLResponse)
async def put_user_password(request: Request):
    return templates.TemplateResponse(request=request, name="user-password-put.html")


@router.post('/create', response_model=TokenInfo)
async def sing_up(user: UserCreate, service: Annotated[ServiceUser, Depends()]):
    res = await service.create_user(user)
    token = await validate_create_user(res)
    return token


@router.post('/token', response_model=TokenInfo)
async def auth(token: Annotated[str, Depends(validate_auth_user)]):
    return token


@router.post(
        '/refresh',
        response_model=TokenInfo,
        response_model_exclude_none=True
    )
async def auth_refresh_jwt(user: Annotated[UserRead, Depends(get_current_auth_user_for_refresh)]):
    ref = await refresh_token_jwt(user)
    return ref


@router.get('/me', response_model=UserRead)
async def get_me(
    payload: Annotated[dict, Depends(get_current_token_payload)],
    me: Annotated[UserRead, Depends(get_current_active_auth_user)]
    ):
    iat =  payload.get("iat")
    return me