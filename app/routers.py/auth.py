from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.models.users import *
from app.core.security import verify_password, get_password_hash,create_access_token
from app.database import get_db
from app.schemas.users import UserCreate, UserRead, UserLogin, Token


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db:AsyncSession=Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed_password = get_password_hash(user_data.password)
    new_user = User(email=user_data.email, hashed_password=hashed_password)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == form_data.email))
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        rate_limit_exceeded = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,   
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

        raise rate_limit_exceeded
    access_token = create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}

    
