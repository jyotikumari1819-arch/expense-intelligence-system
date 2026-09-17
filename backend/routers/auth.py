from fastapi import APIRouter, HTTPException, status
from pymongo.errors import DuplicateKeyError
from bson import ObjectId

from models import UserSignup, UserLogin, Token, ForgotPasswordRequest, ResetPasswordRequest
from database import users_collection
from auth_utils import (
    hash_password,
    verify_password,
    create_access_token,
    create_reset_token,
    verify_reset_token,
)
from email_service import send_password_reset_email

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(payload: UserSignup):
    existing = await users_collection.find_one({"email": payload.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_doc = {
        "name": payload.name,
        "email": payload.email,
        "password": hash_password(payload.password),
    }
    result = await users_collection.insert_one(user_doc)
    token = create_access_token({"sub": str(result.inserted_id)})
    return Token(access_token=token)


@router.post("/login", response_model=Token)
async def login(payload: UserLogin):
    user = await users_collection.find_one({"email": payload.email})
    if not user or not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"sub": str(user["_id"])})
    return Token(access_token=token)


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(payload: ForgotPasswordRequest):
    user = await users_collection.find_one({"email": payload.email})
    # Always return the same response whether or not the email exists —
    # otherwise this endpoint could be used to check which emails are registered.
    if user:
        reset_token = create_reset_token(str(user["_id"]))
        send_password_reset_email(payload.email, reset_token)
    return {"message": "If that email is registered, a reset link has been sent."}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(payload: ResetPasswordRequest):
    user_id = verify_reset_token(payload.token)
    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid or expired reset link")

    result = await users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"password": hash_password(payload.new_password)}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Password reset successful. You can now log in."}
