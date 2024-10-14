from datetime import timedelta

from config import db_helper
from config.config import MINUTES, REFRESH_MINUTES
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from users.models import User
from users.schemas import RefreshToken, Token, UserCreate
from users.services import (authenticate_user, create_access_token,
                            create_refresh_token, create_user,
                            get_user_by_username, validate_token)

router = APIRouter(tags=["Users"], prefix="/user")


@router.post(
    "/create",
)
async def add_user(
    user: UserCreate, db: AsyncSession = Depends(db_helper.session_getter)
):
    """
    Adds a new user to the database.
    """
    return await create_user(user, db)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: UserCreate, db: AsyncSession = Depends(db_helper.session_getter)
):
    """
    Obtaining a JWT token to access the API.
    """
    user = await authenticate_user(
        get_user_by_username, form_data.username, form_data.password, db
    )
    if not user or not isinstance(user, User):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password or username",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=float(MINUTES))
    access_token = create_access_token(
        data={"sub": user.username, "fresh": True}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(minutes=float(REFRESH_MINUTES))
    refresh_token_result = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token_result,
    }


@router.post("/token/refresh", response_model=Token)
async def refresh_token(
    form_data: RefreshToken, db: AsyncSession = Depends(db_helper.session_getter)
):
    """
    Refreshes the JWT token using the refresh token.
    """
    user = await validate_token(db, token=form_data.refresh_token)

    access_token_expires = timedelta(minutes=float(MINUTES))
    access_token = create_access_token(
        data={"sub": user.email, "fresh": False}, expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(minutes=float(REFRESH_MINUTES))
    refresh_token_result = create_refresh_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token_result,
    }
