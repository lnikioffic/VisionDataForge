from pathlib import Path
from typing import Annotated
from fastapi.security import HTTPBearer
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.auth.dependencies import (
    get_current_active_auth_user,
    get_current_token_payload,
)
from src.datasets.paginations import Paginator
from src.datasets.schemas import TypeDatasetRead, DatasetRead
from src.datasets.dependencies import (
    get_count_dataset_for_sale_depend,
    get_types_depend,
    get_dataset_for_sale_depend,
    get_dataset_by_user_id_depend,
    valid_dataset_id,
)
from src.datasets.service import DatasetService
from src.users.schemas import UserRead


http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(tags=['datasets'], dependencies=[Depends(http_bearer)])

router.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')


# Отображает раздела о компании
@router.get('/', response_class=HTMLResponse)
async def get_company_about(
    request: Request,
):
    return templates.TemplateResponse(request=request, name='company-about.html')


# Отображает раздела каталога датасетов
@router.get('/datasets/{page}', response_model=list[DatasetRead])
async def get_company_datasets(
    request: Request,
    page: Annotated[
        int, Path(ge=1, default=1)
    ],  # проверяем, что номер страницы является положительным целым числом
    datasets: Annotated[list[DatasetRead], Depends(get_dataset_for_sale_depend)],
    total_count: Annotated[int, Depends(get_count_dataset_for_sale_depend)],
    per_page: int = 10,
):

    paginator = Paginator(datasets, page, per_page, total_count)

    return templates.TemplateResponse(
        request=request,
        name='company-datasets.html',
        context={
            'request': request,
            'datasets': paginator._items,
            'paginator': paginator,  # передали объект класса Paginator в качестве аргумента paginator
        },
    )


# Отображение датасета
@router.get(
    '/dataset/{dataset_id}', response_class=HTMLResponse, response_model=DatasetRead
)
async def get_company_datasets(
    request: Request, dataset: Annotated[DatasetRead, Depends(valid_dataset_id)]
):
    return templates.TemplateResponse(
        request=request,
        name='company-dataset.html',
        context={
            'dataset': dataset,
        },
    )


# api
@router.get('/get-types-dataset', response_model=list[TypeDatasetRead])
async def get_types_dataset(
    types: Annotated[list[TypeDatasetRead], Depends(get_types_depend)]
):
    return types


@router.get('/get-datasets/{page}', response_model=list[DatasetRead])
async def get_datasets(
    request: Request,
    page: Annotated[
        int, Path(ge=1, default=1)
    ],  # проверяем, что номер страницы является положительным целым числом
    datasets: Annotated[list[DatasetRead], Depends(get_dataset_for_sale_depend)],
    total_count: Annotated[int, Depends(get_count_dataset_for_sale_depend)],
    per_page: int = 10,
):
    paginator = Paginator(datasets, page, per_page, total_count)
    return {
        'request': request,
        'datasets': paginator._items,
        'paginator': paginator,  # передали объект класса Paginator в качестве аргумента paginator
    }


@router.get('/get-datasets-user', response_model=list[DatasetRead])
async def get_datasets_user(
    payload: Annotated[dict, Depends(get_current_token_payload)],
    user: Annotated[UserRead, Depends(get_current_active_auth_user)],
    service: Annotated[DatasetService, Depends()],
):
    dataset = await get_dataset_by_user_id_depend(user.id, service)
    return dataset


@router.get('/get-dataset/{dataset_id}', response_model=DatasetRead)
async def get_dataset(dataset: Annotated[DatasetRead, Depends(valid_dataset_id)]):
    return dataset


@router.get('/download-dataset/{dataset_id}')
async def download_dataset(dataset: Annotated[DatasetRead, Depends(valid_dataset_id)]):
    file = dataset.file_path
    return FileResponse(
        file, filename=Path(file).stem, media_type='multipart/form-data'
    )
