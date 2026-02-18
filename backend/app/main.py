"""
CampusAI – FastAPI Application Entry Point

Configures middleware, routers, exception handlers, and lifespan events.
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.routers import (
    admin,
    auth,
    chat,
    compliance,
    courses,
    documents,
    hostel,
    lms,
    mentor,
    onboarding,
    payments,
    superadmin,
    timetable,
    users,
)
from app.routers import dashboard

settings = get_settings()


# ── Lifespan ─────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup
    print(f"🚀 {settings.APP_NAME} starting in {settings.APP_ENV} mode")
    yield
    # Shutdown
    print(f"👋 {settings.APP_NAME} shutting down")


# ── App Instance ─────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    description="Smart Student Onboarding Platform – Multi-tenant SaaS API",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# ── Middleware ────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ──────────────────────────────────────────────
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["Authentication"])
app.include_router(users.router, prefix=f"{settings.API_V1_PREFIX}/users", tags=["Users"])
app.include_router(onboarding.router, prefix=f"{settings.API_V1_PREFIX}/onboarding", tags=["Onboarding"])
app.include_router(documents.router, prefix=f"{settings.API_V1_PREFIX}/documents", tags=["Documents"])
app.include_router(payments.router, prefix=f"{settings.API_V1_PREFIX}/payments", tags=["Payments"])
app.include_router(hostel.router, prefix=f"{settings.API_V1_PREFIX}/hostel", tags=["Hostel"])
app.include_router(lms.router, prefix=f"{settings.API_V1_PREFIX}/lms", tags=["LMS"])
app.include_router(chat.router, prefix=f"{settings.API_V1_PREFIX}/chat", tags=["AI Assistant"])
app.include_router(courses.router, prefix=f"{settings.API_V1_PREFIX}/courses", tags=["Courses"])
app.include_router(timetable.router, prefix=f"{settings.API_V1_PREFIX}/timetable", tags=["Timetable"])
app.include_router(mentor.router, prefix=f"{settings.API_V1_PREFIX}/mentor", tags=["Mentoring"])
app.include_router(compliance.router, prefix=f"{settings.API_V1_PREFIX}/compliance", tags=["Compliance"])
app.include_router(admin.router, prefix=f"{settings.API_V1_PREFIX}/admin", tags=["Admin"])
app.include_router(superadmin.router, prefix=f"{settings.API_V1_PREFIX}/superadmin", tags=["Super Admin"])
app.include_router(dashboard.router, prefix=f"{settings.API_V1_PREFIX}/dashboard", tags=["Dashboard"])


# ── Health Check ─────────────────────────────────────────
@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "environment": settings.APP_ENV,
    }


# ── Serve local uploads ─────────────────────────────────
uploads_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")
