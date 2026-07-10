import os
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException

from api.deps.database import get_database
from core.config import Settings
from core.security import create_access_token, hash_password
from database.postgre.session import AsyncSession
from schemas.token_bearer import Token
from schemas.auth import UserCreate, UserLogin
from services.auth.auth import create_user, authenticate_user
from database.postgre.crud import get_user_by_email
from core.config import Settings


auth_router = APIRouter()

ACCESS_CODE = Settings.ACCESS_CODE


@auth_router.post("/register")
async def register(user: UserCreate, database: AsyncSession = Depends(get_database)):
    # check existing user by email
    existing = await get_user_by_email(database, user.email)

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    # only allow creating admin if correct access code provided
    role = (user.role or "user").lower()

    if role == "admin":
        if not user.access_code or user.access_code != ACCESS_CODE:
            raise HTTPException(status_code=403, detail="Invalid admin access code")

    hashed_password = hash_password(user.password)

    new_user = await create_user(
        database, user.firstname, user.lastname, user.email, hashed_password, role=role
    )

    return new_user


@auth_router.post("/login")
async def login(
    user: UserLogin, database: AsyncSession = Depends(get_database)
) -> Token:
    authenticated = await authenticate_user(database, user.email, user.password)

    if authenticated is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # include role in token payload
    token = create_access_token(
        {"sub": authenticated.email, "role": getattr(authenticated, "role", "user")},
        timedelta(minutes=int(Settings.ACCESS_TOKEN_EXPIRE_MINUTES)),
    )

    return Token(access_token=token, token_type="bearer")
