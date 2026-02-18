"""
Permission definitions for role-based access control.
"""

from app.models.user import UserRole

# Role hierarchy — higher roles inherit lower role permissions
ROLE_HIERARCHY = {
    UserRole.STUDENT: 1,
    UserRole.ADMIN: 2,
    UserRole.SUPERADMIN: 3,
}


def has_permission(user_role: UserRole, required_role: UserRole) -> bool:
    """Check if a user's role meets the minimum required role level."""
    return ROLE_HIERARCHY.get(user_role, 0) >= ROLE_HIERARCHY.get(required_role, 0)
