import json
from pathlib import Path
from typing import Annotated
from fastapi.security import HTTPBearer
from pydantic import ValidationError
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, status
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.datasets.schemas import TypeDatasetRead
from src.datasets.dependencies import get_types_depend


http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(tags=['datasets'], dependencies=[Depends(http_bearer)])

router.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


#Оотображает раздел с датасетами на продажу
@router.get('/', response_class=HTMLResponse)
async def get_company_datasets(request: Request):
    return templates.TemplateResponse(request=request, name="company-datasets.html")


@router.get('/get-types-dataset', response_model=TypeDatasetRead)
async def get_types_dataset(
    types: Annotated[list[TypeDatasetRead], Depends(get_types_depend)]
) -> list[TypeDatasetRead]:
    return types