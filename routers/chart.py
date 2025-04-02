from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import plotly.graph_objs as go
import plotly.io as pio
from database.storage import get_alerts

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/chart", response_class=HTMLResponse)
async def get_chart(request: Request):
    severity_counts = {"critical": 0, "warning": 0, "info": 0}
    for alert in get_alerts():
        severity_counts[alert.severity] += 1

    colors = {"critical": "red", "warning": "orange", "info": "blue"}
    fig = go.Figure(
        [
            go.Bar(
                x=list(severity_counts.keys()),
                y=list(severity_counts.values()),
                marker=dict(color=[colors[sev] for sev in severity_counts.keys()]),
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
