"""
FollowUp service — scheduling and completion tracking.
"""
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.followup import FollowUp
from app.schemas.followup import FollowUpCreate, FollowUpUpdate


def get_followups(
    db: Session,
    owner_id: int,
    pending_only: bool = False,
) -> list[FollowUp]:
    q = db.query(FollowUp).filter(FollowUp.owner_id == owner_id)
    if pending_only:
        q = q.filter(FollowUp.is_completed == False)
    return q.order_by(FollowUp.scheduled_at.asc()).all()


def get_followup(db: Session, followup_id: int, owner_id: int) -> FollowUp:
    f = db.query(FollowUp).filter(
        FollowUp.id == followup_id, FollowUp.owner_id == owner_id
    ).first()
    if not f:
        raise HTTPException(status_code=404, detail="Follow-up not found")
    return f


def create_followup(db: Session, data: FollowUpCreate, owner_id: int) -> FollowUp:
    f = FollowUp(**data.model_dump(), owner_id=owner_id)
    db.add(f)
    db.commit()
    db.refresh(f)
    return f


def update_followup(
    db: Session, followup_id: int, data: FollowUpUpdate, owner_id: int
) -> FollowUp:
    f = get_followup(db, followup_id, owner_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(f, field, value)
    db.commit()
    db.refresh(f)
    return f


def mark_completed(db: Session, followup_id: int, owner_id: int) -> FollowUp:
    f = get_followup(db, followup_id, owner_id)
    f.is_completed = True
    f.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(f)
    return f


def delete_followup(db: Session, followup_id: int, owner_id: int) -> None:
    f = get_followup(db, followup_id, owner_id)
    db.delete(f)
    db.commit()
