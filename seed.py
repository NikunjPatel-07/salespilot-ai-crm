"""
Seed script — populates the DB with one demo user + realistic sample data.
Run once after migrations:  python seed.py
"""
import sys
import os

# ensure project root is importable
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime, date, timedelta
from app.database import SessionLocal, engine, Base
from app.models import User, Lead, Customer, Deal, FollowUp
from app.models.lead import LeadStatus, LeadSource
from app.models.deal import DealStage
from app.security import hash_password


def seed():
    # Create all tables (safe if already exist)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # ── Guard: skip if already seeded ─────────────────────────────────
    if db.query(User).filter(User.email == "demo@salespilot.io").first():
        print("✓ Database already seeded. Skipping.")
        db.close()
        return

    # ── Demo user ──────────────────────────────────────────────────────
    user = User(
        full_name="Arjun Mehta",
        email="demo@salespilot.io",
        hashed_password=hash_password("demo1234"),
        is_admin=True,
    )
    db.add(user)
    db.flush()   # get user.id before committing

    # ── Leads ──────────────────────────────────────────────────────────
    leads_data = [
        dict(name="Priya Sharma",    email="priya@techvista.in",    phone="+91 98100 11234",
             company="TechVista Solutions", title="Head of Operations",
             status=LeadStatus.qualified,   source=LeadSource.linkedin,  score=78,
             notes="Interested in the enterprise plan. Follows up quickly."),
        dict(name="Rohan Kapoor",    email="rohan.k@finedge.com",   phone="+91 99001 55678",
             company="FinEdge Analytics",  title="VP Finance",
             status=LeadStatus.contacted,  source=LeadSource.referral,   score=55,
             notes="Referred by Priya. Wants a demo next week."),
        dict(name="Sneha Iyer",      email="sneha@cloudnine.io",    phone="+91 80001 77890",
             company="CloudNine SaaS",     title="CTO",
             status=LeadStatus.new,        source=LeadSource.website,    score=30,
             notes="Filled out the contact form. No response yet."),
        dict(name="Amit Desai",      email="amit.d@growthlab.in",   phone=None,
             company="GrowthLab",         title="Founder",
             status=LeadStatus.qualified,  source=LeadSource.event,      score=85,
             notes="Met at SaaS Summit. Very interested. High priority."),
        dict(name="Kavya Nair",      email="kavya@novaretail.com",  phone="+91 97000 33210",
             company="Nova Retail",       title="Marketing Director",
             status=LeadStatus.unqualified, source=LeadSource.cold_email, score=15,
             notes="Not a fit — too small a team for our product tier."),
        dict(name="Dev Malhotra",    email="dev@infinitecorp.io",   phone="+91 91234 56789",
             company="InfiniteCorp",      title="CEO",
             status=LeadStatus.contacted,  source=LeadSource.linkedin,  score=60,
             notes="Engaged with our LinkedIn post. Initial call scheduled."),
    ]

    leads = []
    for ld in leads_data:
        lead = Lead(**ld, owner_id=user.id)
        db.add(lead)
        leads.append(lead)
    db.flush()

    # ── Customers (convert top 2 qualified leads) ──────────────────────
    customer_priya = Customer(
        owner_id=user.id, lead_id=leads[0].id,
        name="Priya Sharma", email="priya@techvista.in",
        phone="+91 98100 11234", company="TechVista Solutions",
        title="Head of Operations", lifetime_value=180000,
        notes="Converted after 2-week trial. Renewed once already.",
    )
    customer_amit = Customer(
        owner_id=user.id, lead_id=leads[3].id,
        name="Amit Desai", email="amit.d@growthlab.in",
        company="GrowthLab", title="Founder", lifetime_value=240000,
        notes="Power user. Potential to upsell to the pro plan.",
    )
    db.add_all([customer_priya, customer_amit])
    leads[0].status = LeadStatus.converted
    leads[3].status = LeadStatus.converted
    db.flush()

    # ── Deals ──────────────────────────────────────────────────────────
    deals_data = [
        dict(customer_id=customer_priya.id, title="TechVista — Enterprise Annual",
             amount=180000, stage=DealStage.won,
             expected_close_date=date.today() - timedelta(days=30),
             notes="Signed. Invoice sent."),
        dict(customer_id=customer_amit.id, title="GrowthLab — Pro Plan Upsell",
             amount=95000, stage=DealStage.negotiation,
             expected_close_date=date.today() + timedelta(days=10),
             notes="Final pricing discussion ongoing."),
        dict(customer_id=customer_priya.id, title="TechVista — Add-on Seats (10)",
             amount=48000, stage=DealStage.proposal,
             expected_close_date=date.today() + timedelta(days=20),
             notes="Waiting on legal review."),
        dict(customer_id=customer_amit.id, title="GrowthLab — Data Sync Module",
             amount=32000, stage=DealStage.prospecting,
             expected_close_date=date.today() + timedelta(days=45),
             notes="Early-stage discussion."),
        dict(customer_id=customer_priya.id, title="TechVista — Year 2 Renewal",
             amount=195000, stage=DealStage.won,
             expected_close_date=date.today() - timedelta(days=5),
             notes="Renewed with a 5% increase."),
    ]
    for dd in deals_data:
        db.add(Deal(**dd, owner_id=user.id))

    # ── Follow-ups ─────────────────────────────────────────────────────
    fu_data = [
        dict(lead_id=leads[1].id, subject="Send demo recording to Rohan",
             scheduled_at=datetime.utcnow() + timedelta(days=1),
             notes="He prefers async review first."),
        dict(lead_id=leads[2].id, subject="Follow up on contact form — Sneha",
             scheduled_at=datetime.utcnow() + timedelta(days=2),
             notes="Try phone if no email reply."),
        dict(lead_id=leads[5].id, subject="Initial discovery call — Dev Malhotra",
             scheduled_at=datetime.utcnow() + timedelta(hours=4),
             notes="30-min call. Use enterprise deck."),
        dict(lead_id=leads[0].id, subject="Quarterly check-in — Priya",
             scheduled_at=datetime.utcnow() - timedelta(days=2),
             is_completed=True,
             completed_at=datetime.utcnow() - timedelta(days=2, hours=-1),
             notes="Discussed renewal. Happy with the product."),
    ]
    for fd in fu_data:
        db.add(FollowUp(**fd, owner_id=user.id))

    db.commit()
    db.close()

    print("✓ Seed data inserted successfully!")
    print("  Login → email: demo@salespilot.io  |  password: demo1234")


if __name__ == "__main__":
    seed()
