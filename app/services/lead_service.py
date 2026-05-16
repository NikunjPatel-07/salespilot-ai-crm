"""
Lead service — all CRUD operations for leads.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.lead import Lead, LeadStatus, LeadSource
from app.schemas.lead import LeadCreate, LeadUpdate


def get_leads(
    db: Session,
    owner_id: int,
    status: LeadStatus | None = None,
    source: LeadSource | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 50,
) -> list[Lead]:
    q = db.query(Lead).filter(Lead.owner_id == owner_id)
    if status:
        q = q.filter(Lead.status == status)
    if source:
        q = q.filter(Lead.source == source)
    if search:
        like = f"%{search}%"
        q = q.filter(
            Lead.name.ilike(like) | Lead.email.ilike(like) | Lead.company.ilike(like)
        )
    return q.order_by(Lead.created_at.desc()).offset(skip).limit(limit).all()


def get_lead(db: Session, lead_id: int, owner_id: int) -> Lead:
    lead = db.query(Lead).filter(Lead.id == lead_id, Lead.owner_id == owner_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


def create_lead(db: Session, data: LeadCreate, owner_id: int) -> Lead:
    lead = Lead(**data.model_dump(), owner_id=owner_id)
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


def update_lead(db: Session, lead_id: int, data: LeadUpdate, owner_id: int) -> Lead:
    lead = get_lead(db, lead_id, owner_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(lead, field, value)
    db.commit()
    db.refresh(lead)
    return lead


def delete_lead(db: Session, lead_id: int, owner_id: int) -> None:
    lead = get_lead(db, lead_id, owner_id)
    db.delete(lead)
    db.commit()
