from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.videoprocessor.router import router as video_router
from src.auth.router import router as auth_router
from src.users.router import router as users_router
from src.datasets.router import router as dataset_router


app = FastAPI()
app.include_router(video_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(dataset_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        if request.url.path == '/auth/login':
            return templates.TemplateResponse(
                request=request, name='user-login-get.html'
            )
        elif request.url.path == '/auth/registration':
            return templates.TemplateResponse(
                request=request, name='user-registration-get.html'
            )
        else:
            return RedirectResponse(url='/auth/login')
    else:
        return {'detail': str(exc)}


app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')


# Оотображает раздел с информацией о компании
@app.get('/company-about', response_class=HTMLResponse)
async def get_company_about(request: Request):
    return templates.TemplateResponse(request=request, name='company-about.html')


# Отображает раздел с информацией о сотрудничестве с компанией
@app.get('/company-cooperation', response_class=HTMLResponse)
async def get_company_cooperation(request: Request):
    return templates.TemplateResponse(request=request, name='company-cooperation.html')


# Отображает раздел с часто задаваемыми вопросами и ответами на них
@app.get('/user-help', response_class=HTMLResponse)
async def get_user_help(request: Request):
    return templates.TemplateResponse(request=request, name='user-help-get.html')
