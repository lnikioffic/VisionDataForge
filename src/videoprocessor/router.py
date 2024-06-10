import json
import asyncio
from pathlib import Path
from typing import Annotated
from fastapi.security import HTTPBearer
from pydantic import ValidationError
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
    status,
)
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.auth.dependencies import (
    get_current_active_auth_user,
    get_current_token_payload,
)
from src.datasets.dependencies import valid_type_id
from src.datasets.service import TypeDatasetService, DatasetService
from src.users.schemas import UserRead
from src.datasets.schemas import TypeDatasetRead, DatasetCreate
from src.videoprocessor.schemas import FormData, TypeAnnotation, MetaDataVideo
from src.videoprocessor.utils.video_handler import (
    save_video,
    get_fps_hendler,
    VideoHandler,
    start_annotation,
)


http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(prefix='/video', tags=['video'], dependencies=[Depends(http_bearer)])

router.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')


# Отображает раздел аннотации фото (заглушка)
@router.get('/annotation-photo', response_class=HTMLResponse)
async def get_photo_annotation(request: Request):
    return templates.TemplateResponse(request=request, name='annotation-photo.html')


# Отображает раздел с аннотацией видео
@router.get('/annotation-video', response_class=HTMLResponse)
async def get_video_annotation(
    request: Request, user: Annotated[UserRead, Depends(get_current_active_auth_user)]
):
    if user:
        return templates.TemplateResponse(request=request, name='annotation-video.html')


# АПИ запрос для получения fps видео загружаемого пользователем
@router.post('/get-FPS', response_model=MetaDataVideo)
async def get_FPS(
    video: Annotated[UploadFile, File()],
    payload: Annotated[dict, Depends(get_current_token_payload)],
):
    path = await save_video(video)

    meta_data = await get_fps_hendler(path)
    return meta_data


@router.post('/upload')
async def upload(
    video: Annotated[UploadFile, File()],
    jsonData: Annotated[str, Form()],
    payload: Annotated[dict, Depends(get_current_token_payload)],
    user: Annotated[UserRead, Depends(get_current_active_auth_user)],
    service_type: Annotated[TypeDatasetService, Depends()],
    service_dataset: Annotated[DatasetService, Depends()],
):
    try:
        jsonData_obj = json.loads(jsonData)
        form_data = FormData(**jsonData_obj)
        path = await save_video(video)
    except ValidationError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'incorrect data',
        )

    type_annotation = await valid_type_id(form_data.type_annotation_id, service_type)

    if type_annotation is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'incorrect data',
        )

    file = await annotation(path, form_data, user, type_annotation, service_dataset)
    return FileResponse(
        file, filename=Path(file).stem, media_type='multipart/form-data'
    )


async def annotation(
    path: str,
    form_data: FormData,
    user: UserRead,
    type_annotation: TypeDatasetRead,
    service: DatasetService,
):
    video_hand = VideoHandler(path, form_data.frame_data)
    await video_hand.coordinate_adaptation()

    coro = asyncio.to_thread(video_hand.start_processing)
    images = await coro

    file, first_frame, second_frame = await start_annotation(
        images, video_hand.frame_data.names_class, type_annotation.name
    )

    dataset = DatasetCreate(
        name=''.join(form_data.frame_data.names_class),
        price=1,
        count_frames=len(images),
        count_classes=len(form_data.frame_data.names_class),
        file_path=file,
        first_frame=first_frame,
        second_frame=second_frame,
        size='',
    )
    if user.is_superuser:
        dataset.for_sale = True
    await service.create_dataset(dataset, type_annotation.id, user.id)

    return file
