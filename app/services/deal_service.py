"""
Deal service — pipeline CRUD operations.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.deal import Deal, DealStage
from app.schemas.deal import DealCreate, DealUpdate


def get_deals(db: Session, owner_id: int, stage: DealStage | None = None) -> list[Deal]:
    q = db.query(Deal).filter(Deal.owner_id == owner_id)
    if stage:
        q = q.filter(Deal.stage == stage)
    return q.order_by(Deal.created_at.desc()).all()


def get_deal(db: Session, deal_id: int, owner_id: int) -> Deal:
    deal = db.query(Deal).filter(Deal.id == deal_id, Deal.owner_id == owner_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal


def create_deal(db: Session, data: DealCreate, owner_id: int) -> Deal:
    deal = Deal(**data.model_dump(), owner_id=owner_id)
    db.add(deal)
    db.commit()
    db.refresh(deal)
    return deal


def update_deal(db: Session, deal_id: int, data: DealUpdate, owner_id: int) -> Deal:
    deal = get_deal(db, deal_id, owner_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(deal, field, value)
    db.commit()
    db.refresh(deal)
    return deal


def delete_deal(db: Session, deal_id: int, owner_id: int) -> None:
    deal = get_deal(db, deal_id, owner_id)
    db.delete(deal)
    db.commit()
