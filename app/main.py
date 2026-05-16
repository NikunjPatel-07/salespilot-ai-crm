"""
SalesPilot AI CRM — application entry point.
Run with: uvicorn app.main:app --reload
"""
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import (
    auth_router, leads_router, customers_router,
    deals_router, followups_router, ai_router, dashboard_router,
)

app = FastAPI(
    title="SalesPilot AI CRM",
    description="A modern sales CRM with AI-powered insights.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(leads_router)
app.include_router(customers_router)
app.include_router(deals_router)
app.include_router(followups_router)
app.include_router(ai_router)


@app.get("/")
def root():
    return RedirectResponse(url="/dashboard")
