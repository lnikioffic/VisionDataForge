import json
from fastapi import APIRouter, File, Form, UploadFile
from videoprocessor.schemas import FrameData
from videoprocessor.utils.video_handler import save_video, coordinate_adaptation, start_processing, get_fps_hendler

router = APIRouter(prefix='/video', tags=['video'])


@router.post('')
async def video_load():
    return {'message': 'ok'}


#АПИ запрос для получения fps видео загружаемого пользователем
@router.post("/getFPS")
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