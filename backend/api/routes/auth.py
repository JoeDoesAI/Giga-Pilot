import os
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException

from api.deps.db_deps import get_db
from core.config import Settings
from core.security import create_access_token, hash_password
from db.postgre.session import AsyncSession
from schemas.token_bearer import Token
from schemas.auth import UserCreate, UserLogin
from services.auth_service.auth import authenticate_user, create_user


auth_router = APIRouter()

ACCESS_CODE = os.getenv("ACCESS_CODE")


@auth_router.post("/register")
async def register(user:UserCreate,db:AsyncSession = Depends(get_db)):
    old_user = await authenticate_user(db, user.email, user.password)
    

    if old_user:
        raise HTTPException(400, "User already exists")
    
    hashed_password = hash_password(user.password)

    new_user = await create_user(db, user.firstname, user.lastname, user.email, hashed_password)
    
    return new_user


@auth_router.post("/login")
async def login(
                user:UserLogin,
                db:AsyncSession = Depends(get_db)
            )-> Token:
   
    
    authenticated = await authenticate_user(db, user.email, user.password)

    if authenticated is None:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
   
    token = create_access_token(
        {"sub": user.email},
        timedelta(minutes=int(Settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    )

    return Token(access_token=token,token_type="bearer")

