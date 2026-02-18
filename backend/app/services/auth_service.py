"""
Authentication Service

Handles registration, login, token management, email verification.
"""

import re
import secrets
import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt_handler import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from app.config import get_settings
from app.core.security import hash_password, verify_password
from app.models.university import University
from app.models.user import User, UserRole
from app.schemas.auth import (
    LoginRequest,
    MessageResponse,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
    VerifyEmailRequest,
)

settings = get_settings()


class AuthService:
    """Authentication business logic."""

    @staticmethod
    async def register(db: AsyncSession, data: RegisterRequest) -> MessageResponse:
        # 1. Find college by slug or name
        university = None
        if data.university_slug:
            result = await db.execute(
                select(University).where(University.slug == data.university_slug)
            )
            university = result.scalar_one_or_none()
        elif data.college_name:
            result = await db.execute(
                select(University).where(University.name.ilike(f"%{data.college_name}%"))
            )
            university = result.scalar_one_or_none()

        if not university:
            # Auto-create the college for demo
            raw_name = data.college_name or data.university_slug or "Unknown College"
            slug = raw_name.lower().replace(" ", "-").replace("&", "and")[:100]
            slug = re.sub(r"[^a-z0-9-]", "", slug)
            university = University(
                id=uuid.uuid4(),
                name=raw_name,
                slug=slug,
                primary_color="#6366F1",
                secondary_color="#8B5CF6",
                is_active=True,
                subscription_plan="free",
                max_students=500,
            )
            db.add(university)
            await db.flush()

        # 2. Check email uniqueness
        existing = await db.execute(select(User).where(User.email == data.email))
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            )

        # 3. Create user
        user = User(
            id=uuid.uuid4(),
            email=data.email,
            hashed_password=hash_password(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
            phone=data.phone,
            role=UserRole.STUDENT,
            university_id=university.id,
            is_active=True,
            is_email_verified=False,
            email_verification_token=secrets.token_urlsafe(32),
        )
        db.add(user)
        await db.flush()

        return MessageResponse(
            message="Account created successfully! You can now sign in.",
            success=True,
        )

    @staticmethod
    async def login(db: AsyncSession, data: LoginRequest) -> TokenResponse:
        # 1. Find user by email
        result = await db.execute(select(User).where(User.email == data.email))
        user = result.scalar_one_or_none()
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )

        # 2. Check active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your account has been deactivated. Contact admin.",
            )

        # 3. Generate tokens
        token_data = {"sub": str(user.id), "role": user.role.value}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        # 4. Store refresh token & update last login
        user.refresh_token = refresh_token
        user.last_login_at = datetime.now(timezone.utc)
        await db.flush()

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    @staticmethod
    async def refresh_token(db: AsyncSession, data: RefreshTokenRequest) -> TokenResponse:
        # 1. Decode refresh token
        payload = decode_refresh_token(data.refresh_token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token.",
            )

        # 2. Find user
        user_id = payload.get("sub")
        result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
        user = result.scalar_one_or_none()
        if not user or user.refresh_token != data.refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token.",
            )

        # 3. Generate new tokens
        token_data = {"sub": str(user.id), "role": user.role.value}
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        user.refresh_token = refresh_token
        await db.flush()

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    @staticmethod
    async def verify_email(db: AsyncSession, data: VerifyEmailRequest) -> MessageResponse:
        result = await db.execute(
            select(User).where(User.email_verification_token == data.token)
        )
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired verification token.",
            )

        user.is_email_verified = True
        user.email_verification_token = None
        await db.flush()

        return MessageResponse(message="Email verified successfully!", success=True)
