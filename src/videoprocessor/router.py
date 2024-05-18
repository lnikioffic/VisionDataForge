import json
from pathlib import Path
from typing import Annotated
from fastapi.security import HTTPBearer
from pydantic import ValidationError
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, status
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.auth.dependencies import get_current_active_auth_user, get_current_token_payload
from src.users.schemas import UserRead
from src.videoprocessor.schemas import FormData, TypeAnnotation
from src.videoprocessor.utils.video_handler import (save_video,   
                                                    get_fps_hendler,
                                                    VideoHandler,
                                                    start_annotation
                                                    )



http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(prefix='/video', tags=['video'], dependencies=[Depends(http_bearer)])

router.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


#Отображает раздел аннотации фото (заглушка)
@router.get("/annotation-photo", response_class=HTMLResponse)
async def get_photo_annotation(request: Request):
    return templates.TemplateResponse(request=request, name="annotation-photo.html")


#Отображает раздел с аннотацией видео
@router.get("/annotation-video", response_class=HTMLResponse)
async def get_video_annotation(request: Request):
    return templates.TemplateResponse(request=request, name="annotation-video.html")


#АПИ запрос для получения fps видео загружаемого пользователем
@router.post("/get-FPS")
async def get_FPS(
    video: Annotated[UploadFile, File()], 
    payload: Annotated[dict, Depends(get_current_token_payload)]
):
    path = await save_video(video)
    
    fps = await get_fps_hendler(path)
    return {"fps": fps}


@router.post('/upload')
async def upload(
    video: Annotated[UploadFile, File()], 
    jsonData: Annotated[str, Form()],
    payload: Annotated[dict, Depends(get_current_token_payload)],
    me: Annotated[UserRead, Depends(get_current_active_auth_user)]
):
    try:        
        jsonData_obj = json.loads(jsonData)
        form_data = FormData(**jsonData_obj)
        path = await save_video(video)
    except ValidationError as ex: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"incorrect data",
        )

    video_hand = VideoHandler(path, form_data.frame_data)
    await video_hand.coordinate_adaptation()
    images = await video_hand.start_processing()

    if form_data.type_annotation == TypeAnnotation.yolo_dark:
        file = await start_annotation(images, video_hand.frame_data.names_class)
        
    filena = Path(file).stem

    return FileResponse(file, filename=Path(file).stem, media_type='multipart/form-data')