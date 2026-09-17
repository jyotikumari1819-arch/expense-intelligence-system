from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId

from models import ExpenseCreate, ExpenseUpdate, ExpenseOut
from database import expenses_collection
from auth_utils import get_current_user
from ai_service import categorize_expense

router = APIRouter(prefix="/expenses", tags=["expenses"])


def _serialize(doc) -> ExpenseOut:
    return ExpenseOut(
        id=str(doc["_id"]),
        amount=doc["amount"],
        description=doc["description"],
        category=doc["category"],
        date=doc["date"],
    )


@router.post("", response_model=ExpenseOut, status_code=201)
async def create_expense(payload: ExpenseCreate, user: dict = Depends(get_current_user)):
    category = payload.category or await categorize_expense(payload.description)

    doc = {
        "user_id": str(user["_id"]),
        "amount": payload.amount,
        "description": payload.description,
        "category": category,
        "date": payload.date or datetime.utcnow(),
    }
    result = await expenses_collection.insert_one(doc)
    doc["_id"] = result.inserted_id
    return _serialize(doc)


@router.get("", response_model=List[ExpenseOut])
async def list_expenses(
    category: Optional[str] = None,
    month: Optional[int] = None,
    year: Optional[int] = None,
    user: dict = Depends(get_current_user),
):
    query = {"user_id": str(user["_id"])}
    if category:
        query["category"] = category

    cursor = expenses_collection.find(query).sort("date", -1)
    results = []
    async for doc in cursor:
        if month and doc["date"].month != month:
            continue
        if year and doc["date"].year != year:
            continue
        results.append(_serialize(doc))
    return results


@router.put("/{expense_id}", response_model=ExpenseOut)
async def update_expense(expense_id: str, payload: ExpenseUpdate, user: dict = Depends(get_current_user)):
    existing = await expenses_collection.find_one({"_id": ObjectId(expense_id), "user_id": str(user["_id"])})
    if not existing:
        raise HTTPException(status_code=404, detail="Expense not found")

    update_data = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
    if update_data:
        await expenses_collection.update_one({"_id": ObjectId(expense_id)}, {"$set": update_data})

    updated = await expenses_collection.find_one({"_id": ObjectId(expense_id)})
    return _serialize(updated)


@router.delete("/{expense_id}", status_code=204)
async def delete_expense(expense_id: str, user: dict = Depends(get_current_user)):
    result = await expenses_collection.delete_one({"_id": ObjectId(expense_id), "user_id": str(user["_id"])})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Expense not found")
