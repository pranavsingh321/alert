from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from routers import alert, chart

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
# Jinja2 templates setup
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


# Load routers
app.include_router(alert.router)
app.include_router(chart.router)
