from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

app = FastAPI()

# Mount the static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


# Generate sample time series data
def generate_time_series():
    dates = [datetime.now() - timedelta(days=i) for i in range(100)]
    values = np.random.randn(100).cumsum()
    return {
        "x": [d.strftime("%Y-%m-%d") for d in dates],
        "y": values,
        "type": "scatter",
        "mode": "lines",
    }


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@app.get("/chart", response_class=HTMLResponse)
async def get_chart(request: Request):
    return templates.TemplateResponse("partials/chart.html", {"request": request})


@app.get("/chart-data", response_class=JSONResponse)
async def get_chart_data():
    # Generate time series data
    return JSONResponse(content=generate_time_series())
