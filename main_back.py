# main.py (FastAPI Backend)
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from datetime import datetime
import json
import numpy as np
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Optional

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Mock OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str


async def get_current_user(token: str = Depends(oauth2_scheme)):
    # In real implementation, validate token here
    return User(username="demo_user")


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


# Mock database
alerts_db = []
alert_id_counter = 1


@app.get("/auth/user")
async def get_user(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username}


@app.get("/api/alerts", response_class=HTMLResponse)
async def get_alerts(request: Request, current_user: User = Depends(get_current_user)):
    return app.state.template_env.get_template("alerts_list.html").render(
        alerts=alerts_db, request=request
    )


@app.post("/api/alerts", response_class=HTMLResponse)
async def create_alert(
    alert: AlertCreate, current_user: User = Depends(get_current_user)
):
    global alert_id_counter
    new_alert = Alert(
        id=alert_id_counter,
        created_at=datetime.now(),
        created_by=current_user.username,
        **alert.dict(),
    )
    alerts_db.append(new_alert)
    alert_id_counter += 1
    return app.state.template_env.get_template("alert_card.html").render(
        alert=new_alert
    )


@app.post("/api/alerts/evaluate/{alert_id}", response_class=HTMLResponse)
async def evaluate_alert(alert_id: int, current_user: User = Depends(get_current_user)):
    alert = next((a for a in alerts_db if a.id == alert_id), None)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    # Simulate evaluation with random data
    time_series = generate_time_series_data()
    alert.state = (
        "firing" if any(y > alert.threshold for y in time_series["y"]) else "ok"
    )

    return app.state.template_env.get_template("alert_card.html").render(alert=alert)


@app.get("/api/alerts/{alert_id}/graph", response_class=HTMLResponse)
async def get_alert_graph(alert_id: int):
    alert = next((a for a in alerts_db if a.id == alert_id), None)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    time_series = generate_time_series_data()
    fig = {
        "data": [
            {
                "x": time_series["time"],
                "y": time_series["y"],
                "type": "scatter",
                "name": alert.query,
            }
        ],
        "layout": {"title": f"Alert {alert.name} Data", "showlegend": True},
    }

    return f"""
    <div class="alert-graph">
        <div id="graph-{alert_id}"></div>
        <script>
            Plotly.newPlot('graph-{alert_id}', {json.dumps(fig['data'])}, {json.dumps(fig['layout'])});
        </script>
    </div>
    """


def generate_time_series_data():
    x = np.arange(50)
    return {
        "time": [datetime.now().timestamp() - 50 * 60 + i * 60 for i in range(50)],
        "y": np.sin(x / 5) * 10 + np.random.randn(50) * 2,
    }
