"""
CampusAI - Authentication Module
Handles user registration, login, password hashing, and session management.
"""
import os
import hashlib
import secrets
from datetime import datetime

from sqlalchemy.orm.session import Session


from models import User, Student
from database import get_session


SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key")
ADMIN_CODE: str = os.getenv("ADMIN_REGISTRATION_CODE", "CAMPUS2026")


def hash_password(password):
    salt: str = secrets.token_hex(16)
    hashed: str = hashlib.sha256((salt + password).encode()).hexdigest()
    return salt + ":" + hashed


def verify_password(password, stored_hash):
    if ":" not in stored_hash:
        return False
    parts = stored_hash.split(":", 1)
    salt = parts[0]
    expected = parts[1]
    actual: str = hashlib.sha256((salt + password).encode()).hexdigest()
    return actual == expected


def register_user(name, email, password, role, admin_code=""):
    """Register a new user."""
    if not name or not email or not password:
        return False, "All fields are required."

    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    if role == "admin" and admin_code != ADMIN_CODE:
        return False, "Invalid admin registration code."

    session: Session = get_session()
    try:
        existing: User | None = session.query(User).filter(User.email == email).first()
        if existing:
            return False, "An account with this email already exists."

        password_hashed: str = hash_password(password)
        new_user = User(
            name=name,
            email=email,
            password_hash=password_hashed,
            role=role,
            created_at=datetime.utcnow()
        )
        session.add(new_user)
        session.flush()

        if role == "student":
            student_profile = Student(
                user_id=new_user.id,
                onboarding_stage=1
            )
            session.add(student_profile)

        session.commit()
        return True, "Account created successfully! Please login."
    except Exception as e:
        session.rollback()
        return False, "Registration failed: " + str(e)
    finally:
        session.close()


def login_user(email, password):
    """Authenticate user."""
    if not email or not password:
        return False, "Email and password are required."

    session: Session = get_session()
    try:
        user: User | None = session.query(User).filter(User.email == email).first()
        if not user:
            return False, "Invalid email or password."

        if not verify_password(password, user.password_hash):
            return False, "Invalid email or password."

        user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": str(user.created_at)
        }

        if user.role == "student" and user.student:
            user_data["student_id"] = user.student.id

        return True, user_data
    except Exception as e:
        return False, "Login failed: " + str(e)
    finally:
        session.close()


def get_user_by_id(user_id):
    """Get user by ID."""
    session: Session = get_session()
    try:
        user: User | None = session.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    finally:
        session.close()
