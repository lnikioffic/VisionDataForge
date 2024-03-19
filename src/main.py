from fastapi import FastAPI
import uvicorn

from videoprocessor.router import router as video_router
from videoprocessor.utils.video_handler import create_test

app = FastAPI()
app.include_router(video_router)


@app.get('/')
async def hello():
    return {'message': 'Hello'}


if __name__ == '__main__':
    create_test(pa='../data/video/n.mp4')
    # uvicorn.run(
    #     app='main:app',
    #     reload=True
    # )