"""
Tenant Resolution Middleware

Resolves the current university tenant from the request context.
Used to enforce multi-tenant data isolation.
"""

from fastapi import Request

from app.config import get_settings

settings = get_settings()


async def resolve_tenant(request: Request):
    """
    Resolve tenant (university) from:
    1. X-Tenant-Slug header
    2. Subdomain (e.g., mit.campusai.com)
    3. Authenticated user's university_id

    Implementation: Phase 4 (multi-tenant enforcement)
    """
    tenant_slug = request.headers.get("X-Tenant-Slug")
    if tenant_slug:
        request.state.tenant_slug = tenant_slug
    else:
        request.state.tenant_slug = None
