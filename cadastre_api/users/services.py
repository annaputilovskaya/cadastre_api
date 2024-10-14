import os
from datetime import datetime, timedelta
from typing import Callable, Union

import jwt
from config import db_helper
from config.config import MINUTES
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from users.models import User
from users.schemas import UserCreate

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


async def create_user(user: UserCreate, db: AsyncSession):
    """
    Creates a new user in the database.
    """
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_admin=False,
    )
    db.add(db_user)
    try:
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"message": "User already exists"},
        )


async def get_user_by_username(username: str, db: AsyncSession):
    """
    Get user data by user username.
    """
    stmt = select(User).filter(User.username == username)
    db_users = await db.scalars(stmt)
    db_user = db_users.first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Creates JWT access token for specified data and optional expiration time.
    """
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=float(MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, os.getenv("SECRET"), algorithm=os.getenv("ALGORITHM")
        )
        return encoded_jwt
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Token creating error"},
        )


def create_refresh_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create a refresh token for the given data and optional expiration time.
    """
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, os.getenv("SECRET"), algorithm=os.getenv("ALGORITHM")
        )
        return encoded_jwt
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Token creating error"},
        )


def verify_password(plain_password, hashed_password) -> bool:
    """
    Verify password against hashed password.
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(
    user: Callable, user_id: str, password: str, db: AsyncSession
) -> Union[User, bool]:
    """
    User authentication method for authenticating.
    """
    user = await user(user_id, db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(db_helper.session_getter),
) -> User:
    """
    Uses OAuth2PasswordBearer to authenticate a user.
    """
    exception = HTTPException(
        status_code=401,
        detail="Не удалось подтвердить подлинность токена",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded_jwt = jwt.decode(
            token, os.getenv("SECRET"), algorithms=[os.getenv("ALGORITHM")]
        )
        username = decoded_jwt.get("sub")
        if username is None:
            raise exception
    except jwt.PyJWTError:
        raise exception
    user = await get_user_by_username(username, db)
    if user is None:
        raise exception
    return user


async def validate_token(db: AsyncSession, token: str = Depends(oauth2_scheme)):
    """
    Validates the JWT token and returns the user object.
    """
    user = await get_current_user(token, db)
    return user
