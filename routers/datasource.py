from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database.storage import add_datasource, get_datasources

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/datasources", response_class=HTMLResponse)
async def list_datasources(request: Request):
    return templates.TemplateResponse(
        "partials/datasources.html",
        {"request": request, "datasources": get_datasources()},
    )


@router.post("/datasources")
async def create_datasource(
    request: Request, name: str = Form(...), url: str = Form(...)
):
    add_datasource(name, url)
    return templates.TemplateResponse(
        "partials/datasources.html",
        {"request": request, "datasources": get_datasources()},
    )
