"""
Deals router — pipeline management with stage filtering.
"""
from fastapi import APIRouter, Depends, Request, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.deal import DealStage
from app.models.customer import Customer
from app.schemas.deal import DealCreate, DealUpdate, DealOut
from app.services.deal_service import (
    get_deals, get_deal, create_deal, update_deal, delete_deal,
)
from app.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/deals", tags=["deals"])
templates = Jinja2Templates(directory="app/templates")


# ── REST API ────────────────────────────────────────────────────────────────────

@router.get("/api", response_model=list[DealOut])
def api_list(
    stage: DealStage | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_deals(db, current_user.id, stage)


@router.post("/api", response_model=DealOut, status_code=201)
def api_create(
    data: DealCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_deal(db, data, current_user.id)


@router.put("/api/{deal_id}", response_model=DealOut)
def api_update(
    deal_id: int, data: DealUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_deal(db, deal_id, data, current_user.id)


@router.delete("/api/{deal_id}", status_code=204)
def api_delete(
    deal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_deal(db, deal_id, current_user.id)


# ── HTML views ──────────────────────────────────────────────────────────────────

@router.get("/", response_class=HTMLResponse)
def deals_page(
    request: Request,
    stage: str = Query(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stage_filter = DealStage(stage) if stage else None
    deals = get_deals(db, current_user.id, stage_filter)
    # group by stage for kanban view
    pipeline = {s: [] for s in DealStage}
    for deal in deals:
        pipeline[deal.stage].append(deal)
    customers = db.query(Customer).filter(Customer.owner_id == current_user.id).all()
    return templates.TemplateResponse(request, "deals/list.html", {
        "request": request, "deals": deals, "pipeline": pipeline,
        "user": current_user, "stages": list(DealStage),
        "sel_stage": stage, "customers": customers,
    })


@router.get("/new", response_class=HTMLResponse)
def deal_new_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    customers = db.query(Customer).filter(Customer.owner_id == current_user.id).all()
    return templates.TemplateResponse(request, "deals/form.html", {
        "request": request, "user": current_user,
        "deal": None, "customers": customers, "stages": list(DealStage),
    })


@router.post("/new", response_class=HTMLResponse)
def deal_create_submit(
    request: Request,
    title: str = Form(...), customer_id: int = Form(...),
    amount: int = Form(0), stage: str = Form("prospecting"),
    expected_close_date: str = Form(""), notes: str = Form(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from datetime import date
    close_date = date.fromisoformat(expected_close_date) if expected_close_date else None
    data = DealCreate(
        title=title, customer_id=customer_id, amount=amount,
        stage=DealStage(stage), expected_close_date=close_date,
        notes=notes or None,
    )
    create_deal(db, data, current_user.id)
    return RedirectResponse(url="/deals/", status_code=302)


@router.get("/{deal_id}/edit", response_class=HTMLResponse)
def deal_edit_page(
    request: Request, deal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deal = get_deal(db, deal_id, current_user.id)
    customers = db.query(Customer).filter(Customer.owner_id == current_user.id).all()
    return templates.TemplateResponse(request, "deals/form.html", {
        "request": request, "user": current_user,
        "deal": deal, "customers": customers, "stages": list(DealStage),
    })


@router.post("/{deal_id}/edit", response_class=HTMLResponse)
def deal_edit_submit(
    request: Request, deal_id: int,
    title: str = Form(...), amount: int = Form(0),
    stage: str = Form("prospecting"),
    expected_close_date: str = Form(""), notes: str = Form(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from datetime import date
    close_date = date.fromisoformat(expected_close_date) if expected_close_date else None
    data = DealUpdate(
        title=title, amount=amount, stage=DealStage(stage),
        expected_close_date=close_date, notes=notes or None,
    )
    update_deal(db, deal_id, data, current_user.id)
    return RedirectResponse(url="/deals/", status_code=302)


@router.post("/{deal_id}/delete", response_class=HTMLResponse)
def deal_delete(
    deal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_deal(db, deal_id, current_user.id)
    return RedirectResponse(url="/deals/", status_code=302)
