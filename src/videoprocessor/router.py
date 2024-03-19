from fastapi import APIRouter


router = APIRouter(prefix='/video', tags=['video'])


@router.post('')
async def video_load():
    return {'message': 'ok'}