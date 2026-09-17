from datetime import datetime
from collections import defaultdict

from fastapi import APIRouter, Depends

from database import expenses_collection
from auth_utils import get_current_user
from ai_service import generate_monthly_insight

router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("/summary")
async def get_summary(month: int = None, year: int = None, user: dict = Depends(get_current_user)):
    now = datetime.utcnow()
    month = month or now.month
    year = year or now.year

    cursor = expenses_collection.find({"user_id": str(user["_id"])})
    total = 0.0
    by_category = defaultdict(float)
    matched = []

    async for doc in cursor:
        if doc["date"].month == month and doc["date"].year == year:
            total += doc["amount"]
            by_category[doc["category"]] += doc["amount"]
            matched.append(doc)

    return {
        "month": month,
        "year": year,
        "total": round(total, 2),
        "by_category": {k: round(v, 2) for k, v in by_category.items()},
        "transaction_count": len(matched),
    }


@router.get("/monthly")
async def get_monthly_insight(month: int = None, year: int = None, user: dict = Depends(get_current_user)):
    summary = await get_summary(month=month, year=year, user=user)

    cursor = expenses_collection.find({"user_id": str(user["_id"])})
    matched = []
    async for doc in cursor:
        if doc["date"].month == summary["month"] and doc["date"].year == summary["year"]:
            matched.append(doc)

    text = await generate_monthly_insight(matched, summary["total"], summary["by_category"])
    return {**summary, "insight": text}
