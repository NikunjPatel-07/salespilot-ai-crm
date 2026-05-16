"""
AI assistant router — 4 endpoints that call the mock AI service.
All return JSON so they can be called from JS fetch on any page.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.security import get_current_user
from app.models.user import User
from app.models.lead import Lead
from app.services import ai_service

router = APIRouter(prefix="/ai", tags=["ai"])


class AIResponse(BaseModel):
    result: str


def _get_lead(lead_id: int, owner_id: int, db: Session) -> Lead:
    lead = db.query(Lead).filter(Lead.id == lead_id, Lead.owner_id == owner_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@router.get("/followup-message/{lead_id}", response_model=AIResponse)
def followup_message(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    lead = _get_lead(lead_id, current_user.id, db)
    return {"result": ai_service.generate_followup_message(lead)}


@router.get("/cold-pitch/{lead_id}", response_model=AIResponse)
def cold_pitch(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    lead = _get_lead(lead_id, current_user.id, db)
    return {"result": ai_service.generate_cold_pitch(lead)}


@router.get("/next-action/{lead_id}", response_model=AIResponse)
def next_action(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    lead = _get_lead(lead_id, current_user.id, db)
    return {"result": ai_service.suggest_next_action(lead)}


@router.get("/score-explain/{lead_id}", response_model=AIResponse)
def score_explain(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    lead = _get_lead(lead_id, current_user.id, db)
    return {"result": ai_service.explain_lead_score(lead)}
