from fastapi import APIRouter, Depends
from database import DEFAULT_CATEGORIES
from auth_utils import get_current_user

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("")
async def list_categories(user: dict = Depends(get_current_user)):
    return {"categories": DEFAULT_CATEGORIES}
