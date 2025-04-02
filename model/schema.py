from pydantic import BaseModel
from datetime import datetime


class DataSourceCreate(BaseModel):
    name: str
    url: str


class DataSource(DataSourceCreate):
    id: int


class UserCreate(BaseModel):
    username: str
    password: str


class User(UserCreate):
    id: int
    hashed_password: str


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
