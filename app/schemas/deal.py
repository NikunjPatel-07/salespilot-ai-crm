from datetime import datetime, date
from pydantic import BaseModel
from app.models.deal import DealStage


class DealCreate(BaseModel):
    title: str
    customer_id: int
    amount: int = 0          # in rupees / dollars (whole number)
    stage: DealStage = DealStage.prospecting
    expected_close_date: date | None = None
    notes: str | None = None


class DealUpdate(BaseModel):
    title: str | None = None
    amount: int | None = None
    stage: DealStage | None = None
    expected_close_date: date | None = None
    notes: str | None = None


class DealOut(BaseModel):
    id: int
    title: str
    customer_id: int
    amount: int
    stage: DealStage
    expected_close_date: date | None
    notes: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
