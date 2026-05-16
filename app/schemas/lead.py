from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.models.lead import LeadStatus, LeadSource


class LeadCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    company: str | None = None
    title: str | None = None
    status: LeadStatus = LeadStatus.new
    source: LeadSource = LeadSource.other
    score: int = 0
    notes: str | None = None


class LeadUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    company: str | None = None
    title: str | None = None
    status: LeadStatus | None = None
    source: LeadSource | None = None
    score: int | None = None
    notes: str | None = None


class LeadOut(BaseModel):
    id: int
    name: str
    email: str
    phone: str | None
    company: str | None
    title: str | None
    status: LeadStatus
    source: LeadSource
    score: int
    notes: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
