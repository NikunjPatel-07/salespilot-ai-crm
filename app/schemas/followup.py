from datetime import datetime
from pydantic import BaseModel


class FollowUpCreate(BaseModel):
    lead_id: int
    subject: str
    notes: str | None = None
    scheduled_at: datetime


class FollowUpUpdate(BaseModel):
    subject: str | None = None
    notes: str | None = None
    scheduled_at: datetime | None = None
    is_completed: bool | None = None


class FollowUpOut(BaseModel):
    id: int
    lead_id: int
    subject: str
    notes: str | None
    scheduled_at: datetime
    is_completed: bool
    completed_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}
