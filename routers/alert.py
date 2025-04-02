from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database.storage import add_alert, get_alerts

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.post("/alerts", response_class=HTMLResponse)
async def create_alert(
    request: Request,
    name: str = Form(...),
    query: str = Form(...),
    threshold: float = Form(...),
    duration: str = Form("5m"),
    severity: str = Form("critical"),
):
    add_alert(name, query, threshold, duration, severity)
    return templates.TemplateResponse(
        "partials/alerts_list.html", {"request": request, "alerts": get_alerts()}
    )


@router.get("/alerts", response_class=HTMLResponse)
async def get_alerts_view(request: Request):
    return templates.TemplateResponse(
        "partials/alerts_list.html", {"request": request, "alerts": get_alerts()}
    )
