"""
Leads router — REST API + HTML views.
"""
from fastapi import APIRouter, Depends, Request, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.lead import LeadStatus, LeadSource
from app.schemas.lead import LeadCreate, LeadUpdate, LeadOut
from app.services.lead_service import (
    get_leads, get_lead, create_lead, update_lead, delete_lead
)
from app.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/leads", tags=["leads"])
templates = Jinja2Templates(directory="app/templates")


# ── REST API ────────────────────────────────────────────────────────────────────

@router.get("/api", response_model=list[LeadOut])
def api_list_leads(
    status: LeadStatus | None = Query(None),
    source: LeadSource | None = Query(None),
    search: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_leads(db, current_user.id, status, source, search)


@router.post("/api", response_model=LeadOut, status_code=201)
def api_create_lead(
    data: LeadCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_lead(db, data, current_user.id)


@router.get("/api/{lead_id}", response_model=LeadOut)
def api_get_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_lead(db, lead_id, current_user.id)


@router.put("/api/{lead_id}", response_model=LeadOut)
def api_update_lead(
    lead_id: int,
    data: LeadUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_lead(db, lead_id, data, current_user.id)


@router.delete("/api/{lead_id}", status_code=204)
def api_delete_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_lead(db, lead_id, current_user.id)


# ── HTML views ──────────────────────────────────────────────────────────────────

@router.get("/", response_class=HTMLResponse)
def leads_page(
    request: Request,
    search: str = Query(""),
    status: str = Query(""),
    source: str = Query(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    status_filter = LeadStatus(status) if status else None
    source_filter = LeadSource(source) if source else None
    leads = get_leads(db, current_user.id, status_filter, source_filter, search or None)
    return templates.TemplateResponse(request, "leads/list.html", {
        "request": request,
        "leads": leads,
        "user": current_user,
        "statuses": list(LeadStatus),
        "sources": list(LeadSource),
        "search": search,
        "sel_status": status,
        "sel_source": source,
    })


@router.get("/new", response_class=HTMLResponse)
def lead_new_page(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    return templates.TemplateResponse(request, "leads/form.html", {
        "request": request,
        "user": current_user,
        "lead": None,
        "statuses": list(LeadStatus),
        "sources": list(LeadSource),
    })


@router.post("/new", response_class=HTMLResponse)
def lead_create_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    company: str = Form(""),
    title: str = Form(""),
    status: str = Form("new"),
    source: str = Form("other"),
    score: int = Form(0),
    notes: str = Form(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = LeadCreate(
        name=name, email=email, phone=phone or None,
        company=company or None, title=title or None,
        status=LeadStatus(status), source=LeadSource(source),
        score=score, notes=notes or None,
    )
    create_lead(db, data, current_user.id)
    return RedirectResponse(url="/leads/", status_code=302)


@router.get("/{lead_id}/edit", response_class=HTMLResponse)
def lead_edit_page(
    request: Request,
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    lead = get_lead(db, lead_id, current_user.id)
    return templates.TemplateResponse(request, "leads/form.html", {
        "request": request,
        "user": current_user,
        "lead": lead,
        "statuses": list(LeadStatus),
        "sources": list(LeadSource),
    })


@router.post("/{lead_id}/edit", response_class=HTMLResponse)
def lead_edit_submit(
    request: Request,
    lead_id: int,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(""),
    company: str = Form(""),
    title: str = Form(""),
    status: str = Form("new"),
    source: str = Form("other"),
    score: int = Form(0),
    notes: str = Form(""),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = LeadUpdate(
        name=name, email=email, phone=phone or None,
        company=company or None, title=title or None,
        status=LeadStatus(status), source=LeadSource(source),
        score=score, notes=notes or None,
    )
    update_lead(db, lead_id, data, current_user.id)
    return RedirectResponse(url="/leads/", status_code=302)


@router.post("/{lead_id}/delete", response_class=HTMLResponse)
def lead_delete(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_lead(db, lead_id, current_user.id)
    return RedirectResponse(url="/leads/", status_code=302)
