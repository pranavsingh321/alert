from model.schema import User, DataSource, Alert
from datetime import datetime
from core.security import hash_password

datasources = []
ds_id = 1


def add_datasource(name: str, url: str) -> DataSource:
    global ds_id
    new_ds = DataSource(id=ds_id, name=name, url=url)
    datasources.append(new_ds)
    ds_id += 1
    return new_ds


def get_datasources():
    return datasources


users = []
user_id = 1


def add_user(username: str, password: str) -> User:
    global user_id
    hashed_pw = hash_password(password)
    new_user = User(id=user_id, username=username, hashed_password=hashed_pw)
    users.append(new_user)
    user_id += 1
    return new_user


def get_user(username: str) -> User | None:
    for user in users:
        if user.username == username:
            return user
    return None


alerts = []
alert_id = 1


def add_alert(
    name: str, query: str, threshold: float, duration: str, severity: str
) -> Alert:
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
    return new_alert


def get_alerts():
    return alerts
