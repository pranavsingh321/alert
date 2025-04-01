from fastapi import FastAPI, Request, Form, Depends
import plotly.graph_objs as go
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
from typing import List
import plotly.io as pio
import json

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# In-memory storage for alerts
alerts = []
alert_id = 1


class AlertCreate(BaseModel):
    name: str
    query: str
    threshold: float
    duration: str = "5m"
    severity: str = "critical"


class Alert(AlertCreate):
    id: int
    state: str = "pending"
    created_at: datetime
    created_by: str


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@app.post("/alerts", response_class=HTMLResponse)
async def create_alert(
    request: Request,
    name: str = Form(...),
    query: str = Form(...),
    threshold: float = Form(...),
    duration: str = Form("5m"),
    severity: str = Form("critical"),
):
    global alert_id
    new_alert = Alert(
        id=alert_id,
        name=name,
        query=query,
        threshold=threshold,
        duration=duration,
        severity=severity,
        state="pending",
        created_at=datetime.utcnow(),
        created_by="admin",
    )
    alerts.append(new_alert)
    alert_id += 1
    return templates.TemplateResponse(
        "partials/alerts_list.html", {"request": request, "alerts": alerts}
    )


@app.get("/alerts", response_class=HTMLResponse)
async def get_alerts(request: Request):
    return templates.TemplateResponse(
        "partials/alerts_list.html", {"request": request, "alerts": alerts}
    )


@app.get("/chart", response_class=HTMLResponse)
async def get_chart(request: Request):
    severity_counts = {"critical": 0, "warning": 0, "info": 0}
    for alert in alerts:
        severity_counts[alert.severity] += 1

    colors = {"critical": "red", "warning": "orange", "info": "blue"}
    fig = go.Figure(
        [
            go.Bar(
                x=list(severity_counts.keys()),
                y=list(severity_counts.values()),
                marker=dict(
                    color=[colors[sev] for sev in severity_counts.keys()]
                ),  # Assign colors
            )
        ]
    )
    fig.update_layout(
        title="Alerts by Severity", xaxis_title="Severity", yaxis_title="Count"
    )

    plotly_json = pio.to_json(fig)
    return templates.TemplateResponse(
        "partials/chart.html", {"request": request, "plotly_json": plotly_json}
    )
