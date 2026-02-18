"""
CampusAI - Database Configuration
SQLAlchemy engine and session management.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///campus_ai.db")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session():
    """Get a new database session (non-generator)."""
    return SessionLocal()


def init_db() -> None:
    """Create all tables."""
    from models import User, Student, Reminder, ChatHistory, Escalation
    Base.metadata.create_all(bind=engine)
