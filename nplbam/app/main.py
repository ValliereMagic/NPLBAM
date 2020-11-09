from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

# FastAPI and templates engine initialization
nplbam: FastAPI = FastAPI()
templates = Jinja2Templates(directory="nplbam/templates/")


@nplbam.get("/")
async def index_test(request: Request):
    test = "Banana Bread"
    return templates.TemplateResponse('index.html', context={'request': request, 'test': test})
