from fastapi import FastAPI
import uvicorn

from videoprocessor.router import router as video_router
from auth.router import router as auth_router
from users.router import router as users_router

from videoprocessor.utils.video_handler import create_test
from videoprocessor.config import UPLOAD_FOLDER
import os


app = FastAPI()
app.include_router(video_router)
app.include_router(auth_router)
app.include_router(users_router)


@app.get('/')
async def hello():
    return {'message': 'Hello'}


if __name__ == '__main__':
    # dest = os.path.join(UPLOAD_FOLDER, 'n.mp4')
    # print(dest)
    # create_test(dest)
    uvicorn.run(
        app='main:app',
        reload=True
    )