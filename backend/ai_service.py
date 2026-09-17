"""
Thin wrapper around the Gemini API for two jobs:
1. Auto-categorizing an expense from its free-text description.
2. Turning a month's worth of expenses into a short, human-readable summary.

If no GEMINI_API_KEY is set, both functions fall back to simple
rule-based behavior so the app still works without a key.
"""
from typing import List, Dict
from config import settings
from database import DEFAULT_CATEGORIES

_model = None


def _get_model():
    global _model
    if _model is not None:
        return _model
    if not settings.gemini_api_key:
        return None
    import google.generativeai as genai
    genai.configure(api_key=settings.gemini_api_key)
    _model = genai.GenerativeModel("gemini-1.5-flash")
    return _model


def _fallback_categorize(description: str) -> str:
    text = description.lower()
    keyword_map = {
        "Food": ["restaurant", "food", "swiggy", "zomato", "cafe", "grocery", "lunch", "dinner"],
        "Transport": ["uber", "ola", "cab", "bus", "train", "fuel", "petrol", "metro"],
        "Rent": ["rent", "landlord"],
        "Utilities": ["electricity", "water bill", "internet", "wifi", "recharge", "gas bill"],
        "Shopping": ["amazon", "flipkart", "myntra", "clothes", "shopping"],
        "Entertainment": ["movie", "netflix", "spotify", "game", "concert"],
        "Health": ["hospital", "medicine", "pharmacy", "doctor"],
        "Education": ["course", "book", "tuition", "fees", "udemy"],
        "Travel": ["flight", "hotel", "trip", "vacation"],
    }
    for category, keywords in keyword_map.items():
        if any(k in text for k in keywords):
            return category
    return "Other"


async def categorize_expense(description: str) -> str:
    model = _get_model()
    if model is None:
        return _fallback_categorize(description)

    prompt = (
        f"Classify this expense into exactly one of these categories: "
        f"{', '.join(DEFAULT_CATEGORIES)}.\n"
        f"Expense description: \"{description}\"\n"
        f"Reply with only the category name, nothing else."
    )
    try:
        response = model.generate_content(prompt)
        category = response.text.strip()
        return category if category in DEFAULT_CATEGORIES else _fallback_categorize(description)
    except Exception:
        return _fallback_categorize(description)


def _fallback_summary(expenses: List[Dict], total: float, by_category: Dict[str, float]) -> str:
    if not expenses:
        return "No expenses recorded for this period."
    top_category = max(by_category, key=by_category.get) if by_category else "N/A"
    return (
        f"You spent a total of ₹{total:.2f} across {len(expenses)} transactions this month. "
        f"Your biggest spending category was {top_category} (₹{by_category.get(top_category, 0):.2f}). "
        f"Consider reviewing that category if it feels higher than expected."
    )


async def generate_monthly_insight(expenses: List[Dict], total: float, by_category: Dict[str, float]) -> str:
    model = _get_model()
    if model is None:
        return _fallback_summary(expenses, total, by_category)

    breakdown = ", ".join(f"{cat}: ₹{amt:.2f}" for cat, amt in by_category.items())
    prompt = (
        f"You are a friendly personal finance assistant. A user spent a total of ₹{total:.2f} "
        f"this month across {len(expenses)} transactions. Category breakdown: {breakdown}. "
        f"Write a short (3-4 sentence), encouraging, plain-English summary of their spending, "
        f"highlighting the top category and one practical tip if spending seems high in any area."
    )
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return _fallback_summary(expenses, total, by_category)
