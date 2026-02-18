"""
General utility helpers.
"""

import secrets
import string
import uuid
from datetime import datetime, timezone


def generate_token(length: int = 64) -> str:
    """Generate a cryptographically secure random token."""
    return secrets.token_urlsafe(length)


def generate_transaction_id() -> str:
    """Generate a unique transaction ID for payments."""
    return f"TXN-{uuid.uuid4().hex[:12].upper()}"


def utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


def generate_random_password(length: int = 12) -> str:
    """Generate a random password (for LMS activation keys, etc.)."""
    alphabet = string.ascii_letters + string.digits + "!@#$%"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def slugify(text: str) -> str:
    """Convert text to URL-safe slug."""
    import re
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")
