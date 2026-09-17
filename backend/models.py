from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ---------- Auth ----------
class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=6)


class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr


# ---------- Expenses ----------
class ExpenseCreate(BaseModel):
    amount: float = Field(gt=0)
    description: str
    category: Optional[str] = None  # if omitted, AI will auto-categorize
    date: Optional[datetime] = None


class ExpenseUpdate(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    category: Optional[str] = None
    date: Optional[datetime] = None


class ExpenseOut(BaseModel):
    id: str
    amount: float
    description: str
    category: str
    date: datetime


# ---------- Insights ----------
class MonthlyInsightRequest(BaseModel):
    month: Optional[int] = None  # 1-12, defaults to current month
    year: Optional[int] = None
