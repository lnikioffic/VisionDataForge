from fastapi import APIRouter, Request

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse


router = APIRouter(prefix='/users', tags=['users'])

#router.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory="templates")


#Отображает раздел с корзиной пользователя
@router.get("/cart", response_class=HTMLResponse)
async def get_user_cart(request: Request):
    return templates.TemplateResponse(request=request, name="user-cart-get.html")


#О_тображает раздел профиля(базовый шаблон) пользователя
@router.get("/profile", response_class=HTMLResponse)
async def get_user_profile(request: Request):
    return templates.TemplateResponse(request=request, name="user-account-get.html")


#Отображает раздел профиля с информацией об аккаунте пользователя
@router.get("/account", response_class=HTMLResponse)
async def get_user_account(request: Request):
    return templates.TemplateResponse(request=request, name="user-account-get.html")


#Отображает раздел профиля с картами и счетами пользователя
@router.get("/cards-accounts", response_class=HTMLResponse)
async def get_user_cards_accounts(request: Request):
    return templates.TemplateResponse(request=request, name="user-cards-accounts-get.html")


#Отображает раздел профиля с датасетами пользователя
@router.get("/datasets", response_class=HTMLResponse)
async def get_user_datasets(request: Request):
    return templates.TemplateResponse(request=request, name="user-datasets-get.html")




#Отображает раздел профиля с настройками безопасности пользователя
@router.get("/security", response_class=HTMLResponse)
async def get_user_security(request: Request):
    return templates.TemplateResponse(request=request, name="user-security-get.html")

#Отображает раздел профиля с подпиской пользователя
@router.get("/subscriptions", response_class=HTMLResponse)
async def get_user_subscriptions(request: Request):
    return templates.TemplateResponse(request=request, name="user-subscriptions-get.html")





#Отображает раздел для изменения информации об аккаунте пользователя
@router.get("/account-put", response_class=HTMLResponse)
async def put_user_account(request: Request):
    return templates.TemplateResponse(request=request, name="user-account-put.html")

#Отображает раздел для подтверждения удаления аккаунта пользователя
@router.get("/account-delete", response_class=HTMLResponse)
async def delete_user_account(request: Request):
    return templates.TemplateResponse(request=request, name="user-account-delete.html")