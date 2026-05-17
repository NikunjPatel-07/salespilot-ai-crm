"""
Follow-ups router — scheduling, pending view, and mark-complete.
"""
from fastapi import APIRouter, Depends, Request, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.followup import FollowUpCreate, FollowUpUpdate, FollowUpOut
from app.services.followup_service import (
    get_followups, get_followup, create_followup,
    update_followup, mark_completed, delete_followup,
)
from app.services.lead_service import get_leads
from app.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/followups", tags=["followups"])
templates = Jinja2Templates(directory="app/templates")


# ── REST API ────────────────────────────────────────────────────────────────────

@router.get("/api", response_model=list[FollowUpOut])
def api_list(
    pending_only: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_followups(db, current_user.id, pending_only)


@router.post("/api", response_model=FollowUpOut, status_code=201)
def api_create(
    data: FollowUpCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_followup(db, data, current_user.id)


@router.post("/api/{followup_id}/complete", response_model=FollowUpOut)
def api_complete(
    followup_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return mark_completed(db, followup_id, current_user.id)


@router.delete("/api/{followup_id}", status_code=204)
def api_delete(
    followup_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_followup(db, followup_id, current_user.id)


# ── HTML views ──────────────────────────────────────────────────────────────────

@router.get("/", response_class=HTMLResponse)
def followups_page(
    request: Request,
    pending_only: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    followups = get_followups(db, current_user.id, pending_only)
    return templates.TemplateResponse(request, "followups/list.html", {
        "request": request, "followups": followups,
        "user": current_user, "pending_only": pending_only,
    })


@router.get("/new", response_class=HTMLResponse)
def followup_new_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    leads = get_leads(db, current_user.id)
    return templates.TemplateResponse(request, "followups/form.html", {
        "request": request, "user": current_user, "followup": None, "leads": leads,
    })


@router.post("/new", response_class=HTMLResponse)
def followup_create_submit(
    request: Request,
    lead_id: int = Form(...), subject: str = Form(...),
    notes: str = Form(""), scheduled_at: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from datetime import datetime
    data = FollowUpCreate(
        lead_id=lead_id, subject=subject,
        notes=notes or None,
        scheduled_at=datetime.fromisoformat(scheduled_at),
    )
    create_followup(db, data, current_user.id)
    return RedirectResponse(url="/followups/", status_code=302)


@router.post("/{followup_id}/complete", response_class=HTMLResponse)
def followup_complete(
    followup_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    mark_completed(db, followup_id, current_user.id)
    return RedirectResponse(url="/followups/", status_code=302)


@router.post("/{followup_id}/delete", response_class=HTMLResponse)
def followup_delete(
    followup_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_followup(db, followup_id, current_user.id)
    return RedirectResponse(url="/followups/", status_code=302)
