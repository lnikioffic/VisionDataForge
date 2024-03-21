from fastapi import APIRouter, Request

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse


router = APIRouter(prefix='/auth', tags=['auth'])

#router.mount('/static', StaticFiles(directory='static'), name='static')

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