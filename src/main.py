from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get('/')
async def hello():
    return {'message': 'Hello'}

#Отображает раздел с датасетами на продажу (базовый шаблон)
# @app.get("/", response_class=HTMLResponse)
# async def main(request: Request):
#     return templates.TemplateResponse(request=request, name="company-datasets.html")


#Оотображает раздел с информацией о компании
@app.get("/company-about", response_class=HTMLResponse)
async def get_company_about(request: Request):
    return templates.TemplateResponse(request=request, name="company-about.html")


#Оотображает раздел с датасетами на продажу
@app.get("/company-datasets", response_class=HTMLResponse)
async def get_company_datasets(request: Request):
    return templates.TemplateResponse(request=request, name="company-datasets.html")


#Отображает раздел с информацией о сотрудничестве с компанией
@app.get("/company-cooperation", response_class=HTMLResponse)
async def get_company_cooperation(request: Request):
    return templates.TemplateResponse(request=request, name="company-cooperation.html")


#Отображает раздел для карточки датасета компании
@app.get("/company-dataset", response_class=HTMLResponse)
async def get_company_dataset(request: Request):
    return templates.TemplateResponse(request=request, name="company-dataset.html")


#Отображает раздел с часто задаваемыми вопросами и ответами на них
@app.get("/user-help", response_class=HTMLResponse)
async def get_user_help(request: Request):
    return templates.TemplateResponse(request=request, name="user-help-get.html")



if __name__ == '__main__':
    # dest = os.path.join(UPLOAD_FOLDER, 'n.mp4')
    # print(dest)
    # create_test(dest)
    uvicorn.run(
        app='main:app',
        reload=True
    )