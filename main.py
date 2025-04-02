from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routers import alert, chart

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load routers
app.include_router(alerts.router)
app.include_router(charts.router)

# Jinja2 templates setup
templates = Jinja2Templates(directory="templates")
