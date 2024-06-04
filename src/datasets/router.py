import json
from pathlib import Path
from typing import Annotated, List
from fastapi.security import HTTPBearer
from pydantic import ValidationError
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, status
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.auth.dependencies import get_current_active_auth_user, get_current_token_payload
from src.datasets.schemas import TypeDatasetRead, DatasetRead
from src.datasets.dependencies import (
    get_types_depend, 
    get_dataset_for_sale_depend, 
    get_dataset_by_user_id_depend,
    valid_dataset_id
)
from src.datasets.service import DatasetService
from src.users.schemas import UserRead


router = APIRouter(tags=['datasets'])

router.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


#Оотображает раздел с датасетами на продажу
@router.get('/', response_class=HTMLResponse)
async def get_company_datasets(request: Request):
    return templates.TemplateResponse(request=request, name="company-datasets.html")


#Оотображает раздел с датасетами на продажу
@router.get('/dataset/{id}', response_class=HTMLResponse)
async def get_company_datasets(request: Request):
    return templates.TemplateResponse(request=request, name="company-dataset.html")


@router.get('/get-types-dataset', response_model=list[TypeDatasetRead])
async def get_types_dataset(
    types: Annotated[list[TypeDatasetRead], Depends(get_types_depend)]
):
    return types


@router.get('/get-datasets', response_model=list[DatasetRead])
async def get_datasets(dataset: Annotated[list[DatasetRead], Depends(get_dataset_for_sale_depend)]):
    return dataset


@router.get('/get-datasets-user', response_model=list[DatasetRead])
async def get_datasets_user(
    payload: Annotated[dict, Depends(get_current_token_payload)],
    user: Annotated[UserRead, Depends(get_current_active_auth_user)],
    service: Annotated[DatasetService, Depends()]
):
    dataset = await get_dataset_by_user_id_depend(user.id, service)
    return dataset


@router.get('/get-dataset/{dataset_id}', response_model=DatasetRead)
async def get_dataset(dataset: Annotated[DatasetRead, Depends(valid_dataset_id)]):
    return dataset