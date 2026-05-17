"""
Customers router — REST API + HTML views, includes lead-to-customer conversion.
"""
from fastapi import APIRouter, Depends, Request, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerOut
from app.services.customer_service import (
    get_customers, get_customer, create_customer,
    convert_lead_to_customer, update_customer, delete_customer,
)
from app.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/customers", tags=["customers"])
templates = Jinja2Templates(directory="app/templates")


# ── REST API ────────────────────────────────────────────────────────────────────

@router.get("/api", response_model=list[CustomerOut])
def api_list(
    search: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_customers(db, current_user.id, search)


@router.post("/api", response_model=CustomerOut, status_code=201)
def api_create(
    data: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_customer(db, data, current_user.id)


@router.post("/api/convert/{lead_id}", response_model=CustomerOut)
def api_convert(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return convert_lead_to_customer(db, lead_id, current_user.id)


@router.put("/api/{customer_id}", response_model=CustomerOut)
def api_update(
    customer_id: int,
    data: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_customer(db, customer_id, data, current_user.id)


@router.delete("/api/{customer_id}", status_code=204)
def api_delete(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_customer(db, customer_id, current_user.id)


# ── HTML views ──────────────────────────────────────────────────────────────────

@router.get("/", response_class=HTMLResponse)
def customers_page(
    request: Request,
    search: str = Query(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    customers = get_customers(db, current_user.id, search or None)
    return templates.TemplateResponse(request, "customers/list.html", {
        "request": request, "customers": customers,
        "user": current_user, "search": search,
    })


@router.get("/new", response_class=HTMLResponse)
def customer_new_page(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    return templates.TemplateResponse(request, "customers/form.html", {
        "request": request, "user": current_user, "customer": None,
    })


@router.post("/new", response_class=HTMLResponse)
def customer_create_submit(
    request: Request,
    name: str = Form(...), email: str = Form(...),
    phone: str = Form(""), company: str = Form(""),
    title: str = Form(""), notes: str = Form(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = CustomerCreate(
        name=name, email=email,
        phone=phone or None, company=company or None,
        title=title or None, notes=notes or None,
    )
    create_customer(db, data, current_user.id)
    return RedirectResponse(url="/customers/", status_code=302)


@router.get("/{customer_id}/edit", response_class=HTMLResponse)
def customer_edit_page(
    request: Request, customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    customer = get_customer(db, customer_id, current_user.id)
    return templates.TemplateResponse(request, "customers/form.html", {
        "request": request, "user": current_user, "customer": customer,
    })


@router.post("/{customer_id}/edit", response_class=HTMLResponse)
def customer_edit_submit(
    request: Request, customer_id: int,
    name: str = Form(...), email: str = Form(...),
    phone: str = Form(""), company: str = Form(""),
    title: str = Form(""), notes: str = Form(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = CustomerUpdate(
        name=name, email=email,
        phone=phone or None, company=company or None,
        title=title or None, notes=notes or None,
    )
    update_customer(db, customer_id, data, current_user.id)
    return RedirectResponse(url="/customers/", status_code=302)


@router.post("/{customer_id}/delete", response_class=HTMLResponse)
def customer_delete(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_customer(db, customer_id, current_user.id)
    return RedirectResponse(url="/customers/", status_code=302)


@router.post("/convert/{lead_id}", response_class=HTMLResponse)
def convert_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    convert_lead_to_customer(db, lead_id, current_user.id)
    return RedirectResponse(url="/customers/", status_code=302)
