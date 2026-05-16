"""
Auth router — handles register, login (form + JSON), and logout.
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, Request, Response, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, Token
from app.services.auth_service import create_user, authenticate_user
from app.security import create_access_token
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])
templates = Jinja2Templates(directory="app/templates")


# ── REST endpoints (used by API clients / JS fetch) ────────────────────────────

@router.post("/register", response_model=Token)
def api_register(data: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, data)
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token}


@router.post("/token", response_model=Token)
def api_login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, username, password)
    token = create_access_token(
        {"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": token}


# ── HTML form routes ────────────────────────────────────────────────────────────

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
def login_submit(
    request: Request,
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        user = authenticate_user(db, email, password)
    except HTTPException as exc:
        return templates.TemplateResponse(
            "auth/login.html", {"request": request, "error": exc.detail}
        )
    token = create_access_token({"sub": str(user.id)})
    resp = RedirectResponse(url="/dashboard", status_code=302)
    resp.set_cookie("access_token", token, httponly=True, max_age=3600)
    return resp


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.post("/register-form", response_class=HTMLResponse)
def register_submit(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        data = UserCreate(full_name=full_name, email=email, password=password)
        create_user(db, data)
    except HTTPException as exc:
        return templates.TemplateResponse(
            "auth/register.html", {"request": request, "error": exc.detail}
        )
    return RedirectResponse(url="/auth/login?registered=1", status_code=302)


@router.get("/logout")
def logout():
    resp = RedirectResponse(url="/auth/login", status_code=302)
    resp.delete_cookie("access_token")
    return resp
