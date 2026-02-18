"""Seed the database with a test university + users for local development."""

import asyncio
import uuid

from app.config import get_settings
from app.core.security import hash_password
from app.database import async_session
from app.models.university import University
from app.models.user import User, UserRole

settings = get_settings()

UNIVERSITY_ID = uuid.UUID("11111111-1111-1111-1111-111111111111")


async def seed():
    async with async_session() as db:
        # Check if already seeded
        from sqlalchemy import select

        existing = await db.execute(
            select(University).where(University.id == UNIVERSITY_ID)
        )
        if existing.scalar_one_or_none():
            print("✅ Already seeded — skipping")
            return

        # Create university
        uni = University(
            id=UNIVERSITY_ID,
            name="Demo University",
            slug="demo-university",
            domain="demo.edu",
            logo_url="",
            is_active=True,
        )
        db.add(uni)
        await db.flush()

        # Create users
        users = [
            User(
                email="admin@demo.edu",
                hashed_password=hash_password("admin123"),
                first_name="Admin",
                last_name="User",
                role=UserRole.ADMIN,
                university_id=UNIVERSITY_ID,
                is_active=True,
                is_email_verified=True,
            ),
            User(
                email="student@demo.edu",
                hashed_password=hash_password("student123"),
                first_name="Test",
                last_name="Student",
                role=UserRole.STUDENT,
                university_id=UNIVERSITY_ID,
                is_active=True,
                is_email_verified=True,
            ),
            User(
                email="mentor@demo.edu",
                hashed_password=hash_password("mentor123"),
                first_name="Dr.",
                last_name="Mentor",
                role=UserRole.MENTOR,
                university_id=UNIVERSITY_ID,
                is_active=True,
                is_email_verified=True,
            ),
            User(
                email="superadmin@campusai.in",
                hashed_password=hash_password("super123"),
                first_name="Super",
                last_name="Admin",
                role=UserRole.SUPERADMIN,
                university_id=None,
                is_active=True,
                is_email_verified=True,
            ),
        ]
        db.add_all(users)
        await db.commit()
        print("✅ Seeded: Demo University + 4 users")
        print("   📧 admin@demo.edu / admin123")
        print("   📧 student@demo.edu / student123")
        print("   📧 mentor@demo.edu / mentor123")
        print("   📧 superadmin@campusai.in / super123")


if __name__ == "__main__":
    asyncio.run(seed())
