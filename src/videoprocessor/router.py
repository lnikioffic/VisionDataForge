import json
from fastapi import APIRouter, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.videoprocessor.schemas import FrameData
from src.videoprocessor.utils.video_handler import (save_video, 
                                                    coordinate_adaptation, 
                                                    start_processing, 
                                                    get_fps_hendler,
                                                    )

router = APIRouter(prefix='/video', tags=['video'])


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
async def get_FPS(video: UploadFile = File()):
    path = await save_video(video)
    fps = await get_fps_hendler(path, video)
    return {"fps": fps}


@router.post('/uploadtest')
async def upload(video: UploadFile = File()):
    path = await save_video(video)
    return {"filename": video.filename, "path": path}


@router.post('/upload')
async def upload(video: UploadFile = File(), jsonData: str = Form()):
    jsonData_obj = json.loads(jsonData)
    frame_data = FrameData(**jsonData_obj)
    path = await save_video(video)

    await coordinate_adaptation(path, frame_data)

    await start_processing(path, frame_data)

    return {"filename": video.filename, "jsonData": frame_data}