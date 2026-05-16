"""
Mock AI Sales Assistant — runs 100% locally, zero API costs.
Swap the internals for an OpenAI/Gemini call whenever you're ready.
"""
import random
from app.models.lead import Lead


# ─── Canned response pools ────────────────────────────────────────────────────

_FOLLOWUP_TEMPLATES = [
    "Hi {name}, just circling back on our last conversation. Have you had a chance to review the proposal I sent over?",
    "Hey {name}, hope your week is going well! I wanted to follow up and see if you had any questions about {company}.",
    "Hi {name}, I noticed it's been a few days. I'm happy to jump on a quick 15-minute call to address any concerns.",
    "Hello {name}, wanted to check in — are you still interested in exploring how we can help {company} grow?",
    "Hi {name}, just a friendly nudge! Our offer is valid until end of month — let me know if you'd like to move forward.",
]

_COLD_PITCH_TEMPLATES = [
    (
        "Subject: Quick idea for {company}\n\n"
        "Hi {name},\n\n"
        "I came across {company} and was impressed by what you're building. "
        "We've helped similar companies reduce sales cycle time by 30%. "
        "Would you be open to a 15-minute chat this week?\n\nBest,"
    ),
    (
        "Subject: Helping {company} close more deals\n\n"
        "Hi {name},\n\n"
        "I work with sales teams at fast-growing companies to streamline their pipeline. "
        "Given {company}'s trajectory, I thought this might be timely. "
        "Can we connect briefly?\n\nWarm regards,"
    ),
    (
        "Subject: One question for {name}\n\n"
        "Hi {name},\n\n"
        "What's the biggest bottleneck in your current sales process? "
        "I ask because we've solved exactly that for teams like yours at {company}. "
        "Happy to share how — just reply to this email.\n\nCheers,"
    ),
]

_NEXT_ACTIONS = [
    "Send a personalised case study relevant to their industry.",
    "Schedule a live product demo for this week.",
    "Introduce them to a reference customer in the same vertical.",
    "Draft a custom ROI analysis based on their company size.",
    "Follow up with a short Loom video walking through key features.",
    "Share a 2-page comparison sheet against their current solution.",
    "Offer a 14-day free pilot with zero commitment.",
    "Escalate to decision-maker by requesting an executive sponsor meeting.",
]

_SCORE_EXPLANATIONS = {
    (0, 30): [
        "Low engagement so far — no response to outreach. Recommend light touch until there's a signal.",
        "Early stage lead with minimal data. Prioritise qualification before investing time.",
    ],
    (31, 60): [
        "Moderate interest detected. They've engaged but haven't committed. Nurture with value-driven content.",
        "Mid-funnel lead showing some intent. A targeted case study could move the needle.",
    ],
    (61, 100): [
        "High-intent lead — multiple touchpoints and active engagement. Push for a demo or trial ASAP.",
        "Strong buying signals. Don't let this lead go cold — escalate to a closing conversation now.",
    ],
}


# ─── Public API ───────────────────────────────────────────────────────────────

def generate_followup_message(lead: Lead) -> str:
    template = random.choice(_FOLLOWUP_TEMPLATES)
    return template.format(name=lead.name, company=lead.company or "your company")


def generate_cold_pitch(lead: Lead) -> str:
    template = random.choice(_COLD_PITCH_TEMPLATES)
    return template.format(name=lead.name, company=lead.company or "your company")


def suggest_next_action(lead: Lead) -> str:
    return random.choice(_NEXT_ACTIONS)


def explain_lead_score(lead: Lead) -> str:
    score = lead.score
    for (low, high), explanations in _SCORE_EXPLANATIONS.items():
        if low <= score <= high:
            return random.choice(explanations)
    return "Score outside expected range — please recalibrate manually."
