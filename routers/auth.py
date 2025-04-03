from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from database.storage import add_user, get_user
from core.security import verify_password

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("partials/login.html", {"request": request})


@router.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = get_user(username)
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "login.html", {"request": request, "error": "Invalid credentials"}
        )
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="user", value=username)
    return response


@router.post("/register")
async def register(username: str = Form(...), password: str = Form(...)):
    if get_user(username):
        return {"error": "User already exists"}
    add_user(username, password)
    return {"message": "User registered successfully"}


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("partials/register.html", {"request": request})
