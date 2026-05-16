"""
Deal model — tracks revenue pipeline stages.
"""
from datetime import datetime, date
from sqlalchemy import String, Text, Integer, Date, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from app.database import Base


class DealStage(str, enum.Enum):
    prospecting = "prospecting"
    proposal = "proposal"
    negotiation = "negotiation"
    won = "won"
    lost = "lost"


class Deal(Base):
    __tablename__ = "deals"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))

    title: Mapped[str] = mapped_column(String(200))
    amount: Mapped[int] = mapped_column(Integer, default=0)   # stored in cents
    stage: Mapped[DealStage] = mapped_column(
        SAEnum(DealStage), default=DealStage.prospecting
    )
    expected_close_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    owner = relationship("User", back_populates="deals")
    customer = relationship("Customer", back_populates="deals")
