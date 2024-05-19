from typing import Annotated
from fastapi import APIRouter, Depends, Request

from fastapi.security import HTTPBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from src.auth.dependencies import get_current_active_auth_user, get_current_token_payload
from src.users.schemas import UserRead


http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(prefix='/users', tags=['users'], dependencies=[Depends(http_bearer)])

router.mount('/static', StaticFiles(directory='static'), name='static')

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


# #Отображает раздел профиля с картами и счетами пользователя
# @router.get("/cards-accounts", response_class=HTMLResponse)
# async def get_user_cards_accounts(request: Request):
#     return templates.TemplateResponse(request=request, name="user-cards-accounts-get.html")


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

#Отображает раздел для изменения пароля от аккаунта пользователя
@router.get("/password-put", response_class=HTMLResponse)
async def put_user_account(request: Request):
    return templates.TemplateResponse(request=request, name="user-password-put.html")

#Отображает раздел для подтверждения удаления аккаунта пользователя
@router.get("/account-delete", response_class=HTMLResponse)
async def delete_user_account(request: Request):
    return templates.TemplateResponse(request=request, name="user-account-delete.html")


#Отображает раздел для карточки датасета пользователя
@router.get("/dataset/{id}", response_class=HTMLResponse)
async def get_user_dataset(request: Request, id: int):
    return templates.TemplateResponse(request=request, name="user-dataset-get.html")



# #Отображает раздел для добавления карты пользователя
# @router.get("/cards-post", response_class=HTMLResponse)
# async def post_user_cards(request: Request):
#     return templates.TemplateResponse(request=request, name="user-cards-post.html")

# #Отображает раздел для добавления счета пользователя
# @router.get("/accounts-post", response_class=HTMLResponse)
# async def post_user_accounts(request: Request):
#     return templates.TemplateResponse(request=request, name="user-accounts-post.html")


@router.get('/me', response_model=UserRead)
async def get_me(
    payload: Annotated[dict, Depends(get_current_token_payload)],
    me: Annotated[UserRead, Depends(get_current_active_auth_user)]
    ):
    iat =  payload.get("iat")
    return me


@router.get('/me/datasets')
async def get_me_datasets(
    payload: Annotated[dict, Depends(get_current_token_payload)],
    me: Annotated[UserRead, Depends(get_current_active_auth_user)]
    ):
    pass