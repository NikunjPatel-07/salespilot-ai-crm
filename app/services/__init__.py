from app.services.auth_service import create_user, authenticate_user
from app.services.lead_service import (
    get_leads, get_lead, create_lead, update_lead, delete_lead
)
from app.services.customer_service import (
    get_customers, get_customer, create_customer,
    convert_lead_to_customer, update_customer, delete_customer
)
from app.services.deal_service import (
    get_deals, get_deal, create_deal, update_deal, delete_deal
)
from app.services.followup_service import (
    get_followups, get_followup, create_followup,
    update_followup, mark_completed, delete_followup
)
