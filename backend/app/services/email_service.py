"""
Email Service

Handles transactional email sending (verification, notifications).
Uses print logging as placeholder — swap with real SMTP/SendGrid in production.
"""

import logging

from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class EmailService:
    """Email sending business logic."""

    @staticmethod
    async def send_verification_email(to_email: str, token: str, name: str):
        """Send email verification link to new user."""
        verification_url = f"{settings.SUPABASE_URL}/verify?token={token}"
        logger.info(
            f"[EMAIL] Verification email to {to_email}: {verification_url}"
        )
        # In production, integrate with SendGrid/SES/Resend here

    @staticmethod
    async def send_password_reset_email(to_email: str, token: str, name: str):
        """Send password reset link."""
        logger.info(f"[EMAIL] Password reset email to {to_email}")

    @staticmethod
    async def send_document_status_email(
        to_email: str, name: str, document_type: str, status: str
    ):
        """Notify student about document review result."""
        logger.info(
            f"[EMAIL] Document {document_type} {status} notification to {to_email}"
        )

    @staticmethod
    async def send_hostel_allocation_email(
        to_email: str, name: str, room_number: str, block: str
    ):
        """Notify student about hostel room allocation."""
        logger.info(
            f"[EMAIL] Hostel allocation (Room {room_number}, Block {block}) to {to_email}"
        )
