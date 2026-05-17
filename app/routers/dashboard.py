"""
Dashboard router — aggregates key sales metrics for the home view.
"""
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.security import get_current_user
from app.models.user import User
from app.models.lead import Lead
from app.models.customer import Customer
from app.models.deal import Deal, DealStage
from app.models.followup import FollowUp

router = APIRouter(tags=["dashboard"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    uid = current_user.id

    total_leads = db.query(func.count(Lead.id)).filter(Lead.owner_id == uid).scalar()
    total_customers = db.query(func.count(Customer.id)).filter(Customer.owner_id == uid).scalar()

    won_deals = db.query(Deal).filter(Deal.owner_id == uid, Deal.stage == DealStage.won).all()
    won_count = len(won_deals)
    revenue = sum(d.amount for d in won_deals)

    pending_followups = (
        db.query(func.count(FollowUp.id))
        .filter(FollowUp.owner_id == uid, FollowUp.is_completed == False)
        .scalar()
    )

    # recent leads for the activity feed
    recent_leads = (
        db.query(Lead).filter(Lead.owner_id == uid)
        .order_by(Lead.created_at.desc()).limit(5).all()
    )

    # deal pipeline counts per stage
    pipeline_counts = {}
    for stage in DealStage:
        count = (
            db.query(func.count(Deal.id))
            .filter(Deal.owner_id == uid, Deal.stage == stage)
            .scalar()
        )
        pipeline_counts[stage.value] = count

    upcoming_followups = (
        db.query(FollowUp)
        .filter(FollowUp.owner_id == uid, FollowUp.is_completed == False)
        .order_by(FollowUp.scheduled_at.asc())
        .limit(5).all()
    )

    return templates.TemplateResponse(request, "dashboard.html", {
        "request": request,
        "user": current_user,
        "total_leads": total_leads,
        "total_customers": total_customers,
        "won_count": won_count,
        "revenue": revenue,
        "pending_followups": pending_followups,
        "recent_leads": recent_leads,
        "pipeline_counts": pipeline_counts,
        "upcoming_followups": upcoming_followups,
    })
