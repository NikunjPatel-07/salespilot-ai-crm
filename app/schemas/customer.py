from datetime import datetime
from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    company: str | None = None
    title: str | None = None
    lifetime_value: int = 0
    notes: str | None = None
    lead_id: int | None = None


class CustomerUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    company: str | None = None
    title: str | None = None
    lifetime_value: int | None = None
    notes: str | None = None


class CustomerOut(BaseModel):
    id: int
    name: str
    email: str
    phone: str | None
    company: str | None
    title: str | None
    lifetime_value: int
    notes: str | None
    lead_id: int | None
    created_at: datetime

    model_config = {"from_attributes": True}
