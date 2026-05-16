from app.routers.auth import router as auth_router
from app.routers.leads import router as leads_router
from app.routers.customers import router as customers_router
from app.routers.deals import router as deals_router
from app.routers.followups import router as followups_router
from app.routers.ai_assistant import router as ai_router
from app.routers.dashboard import router as dashboard_router

__all__ = [
    "auth_router", "leads_router", "customers_router",
    "deals_router", "followups_router", "ai_router", "dashboard_router",
]
