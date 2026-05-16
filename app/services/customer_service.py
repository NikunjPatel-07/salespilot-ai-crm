"""
Customer service — CRUD + lead-to-customer conversion.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.customer import Customer
from app.models.lead import Lead, LeadStatus
from app.schemas.customer import CustomerCreate, CustomerUpdate


def get_customers(db: Session, owner_id: int, search: str | None = None) -> list[Customer]:
    q = db.query(Customer).filter(Customer.owner_id == owner_id)
    if search:
        like = f"%{search}%"
        q = q.filter(Customer.name.ilike(like) | Customer.email.ilike(like))
    return q.order_by(Customer.created_at.desc()).all()


def get_customer(db: Session, customer_id: int, owner_id: int) -> Customer:
    c = db.query(Customer).filter(Customer.id == customer_id, Customer.owner_id == owner_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Customer not found")
    return c


def create_customer(db: Session, data: CustomerCreate, owner_id: int) -> Customer:
    c = Customer(**data.model_dump(), owner_id=owner_id)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


def convert_lead_to_customer(db: Session, lead_id: int, owner_id: int) -> Customer:
    lead = db.query(Lead).filter(Lead.id == lead_id, Lead.owner_id == owner_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    # mark lead as converted
    lead.status = LeadStatus.converted
    customer = Customer(
        owner_id=owner_id,
        lead_id=lead.id,
        name=lead.name,
        email=lead.email,
        phone=lead.phone,
        company=lead.company,
        title=lead.title,
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def update_customer(db: Session, customer_id: int, data: CustomerUpdate, owner_id: int) -> Customer:
    c = get_customer(db, customer_id, owner_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(c, field, value)
    db.commit()
    db.refresh(c)
    return c


def delete_customer(db: Session, customer_id: int, owner_id: int) -> None:
    c = get_customer(db, customer_id, owner_id)
    db.delete(c)
    db.commit()
