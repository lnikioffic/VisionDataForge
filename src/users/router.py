from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from src.auth.dependencies import (
    get_current_active_auth_user,
    get_current_token_payload,
)
from src.datasets.dependencies import (
    get_dataset_by_user_id_depend,
    valid_dataset_id,
)
from src.datasets.schemas import DatasetRead
from src.datasets.service import DatasetService
from src.users.schemas import UserRead, UserUpdate, UserUpdatePartial
from src.constants import IMAGE_URL
from src.users.service import UserService


http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(prefix='/users', tags=['users'], dependencies=[Depends(http_bearer)])

router.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')


# Отображает раздел с корзиной пользователя
@router.get('/cart', response_class=HTMLResponse)
async def get_user_cart(request: Request):
    return templates.TemplateResponse(request=request, name='user-cart-get.html')


@router.get('/profile', response_class=HTMLResponse)
async def get_user_profile(
    request: Request, user: Annotated[UserRead, Depends(get_current_active_auth_user)]
):
    return templates.TemplateResponse(
        request=request, name='user-account-get.html', context={'user': user}
    )


# Отображает раздел профиля с информацией об аккаунте пользователя
@router.get('/account', response_class=HTMLResponse)
async def get_user_account(
    request: Request, user: Annotated[UserRead, Depends(get_current_active_auth_user)]
):
    return templates.TemplateResponse(
        request=request, name='user-account-get.html', context={'user': user}
    )


# Отображает раздел профиля с датасетами пользователя
@router.get('/datasets', response_class=HTMLResponse)
async def get_user_datasets(
    request: Request,
    user: Annotated[UserRead, Depends(get_current_active_auth_user)],
    service: Annotated[DatasetService, Depends()],
):
    if user:
        datasets = await get_dataset_by_user_id_depend(user.id, service)
        return templates.TemplateResponse(
            request=request,
            name='user-datasets-get.html',
            context={
                'datasets': datasets,
                'image_url': IMAGE_URL,
            },
        )


# @router.get('/get-datasets-user', response_model=list[DatasetRead])
# async def get_datasets_user(
#     payload: Annotated[dict, Depends(get_current_token_payload)],
#     user: Annotated[UserRead, Depends(get_current_active_auth_user)],
#     service: Annotated[DatasetService, Depends()],
# ):
#     dataset = await get_dataset_by_user_id_depend(user.id, service)
#     return dataset


# Отображает раздел профиля с настройками безопасности пользователя
@router.get('/security', response_class=HTMLResponse)
async def get_user_security(
    request: Request, user: Annotated[UserRead, Depends(get_current_active_auth_user)]
):
    if user:
        return templates.TemplateResponse(
            request=request,
            name='user-security-get.html',
            context={'user': user},
        )


# Отображает раздел для изменения информации об аккаунте пользователя
@router.get('/account-put', response_class=HTMLResponse)
async def put_user_account(
    request: Request, user: Annotated[UserRead, Depends(get_current_active_auth_user)]
):
    if user:
        return templates.TemplateResponse(
            request=request,
            name='user-account-put.html',
            context={'user': user},
        )


# Отображает раздел для изменения пароля от аккаунта пользователя
@router.get('/password-put', response_class=HTMLResponse)
async def put_user_account(
    request: Request, user: Annotated[UserRead, Depends(get_current_active_auth_user)]
):
    if user:
        return templates.TemplateResponse(
            request=request, name='user-password-put.html'
        )


# Отображает раздел для подтверждения удаления аккаунта пользователя
@router.get('/account-delete', response_class=HTMLResponse)
async def delete_user_account(
    request: Request, user: Annotated[UserRead, Depends(get_current_active_auth_user)]
):
    if user:
        return templates.TemplateResponse(
            request=request, name='user-account-delete.html'
        )


# Отображает раздел для карточки датасета пользователя
@router.get('/dataset/{dataset_id}', response_class=HTMLResponse)
async def get_user_dataset(
    request: Request,
    user: Annotated[UserRead, Depends(get_current_active_auth_user)],
    dataset: Annotated[DatasetRead, Depends(valid_dataset_id)],
):
    if user:
        return templates.TemplateResponse(
            request=request,
            name='user-dataset-get.html',
            context={
                'dataset': dataset,
                'image_url': IMAGE_URL,
            },
        )


@router.patch('/update-user')
async def update_user_partial(
    user_update: UserUpdatePartial,
    user: Annotated[UserRead, Depends(get_current_active_auth_user)],
    service: Annotated[UserService, Depends()],
) -> UserRead:
    return await service.update_user(user=user, user_update=user_update, partial=True)


@router.put('/update-user')
async def update_user(
    user_update: UserUpdate,
    user: Annotated[UserRead, Depends(get_current_active_auth_user)],
    service: Annotated[UserService, Depends()],
) -> UserRead:
    return await service.update_user(user=user, user_update=user_update)
