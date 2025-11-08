from enum import Enum
from typing import Dict, Set

from app.models.domain.user import RoleType


class Permission(str, Enum):
    # User management permissions (Admin only)
    MANAGE_USERS = "manage_users"
    ACTIVATE_USER = "activate_user"
    DEACTIVATE_USER = "deactivate_user"
    VIEW_ALL_USERS = "view_all_users"

    # User viewing permissions
    VIEW_USER_PROFILE = "view_user_profile"

    # Book permissions
    CREATE_BOOK = "create_book"
    VIEW_BOOK = "view_book"
    EDIT_BOOK = "edit_book"
    EDIT_OWN_BOOK = "edit_own_book"
    DELETE_BOOK = "delete_book"
    DELETE_OWN_BOOK = "delete_own_book"

    # Reading entry permissions
    CREATE_READING_ENTRY = "create_reading_entry"
    VIEW_READING_ENTRY = "view_reading_entry"
    VIEW_OWN_READING_ENTRIES = "view_own_reading_entries"
    EDIT_READING_ENTRY = "edit_reading_entry"
    EDIT_OWN_READING_ENTRY = "edit_own_reading_entry"
    DELETE_READING_ENTRY = "delete_reading_entry"
    DELETE_OWN_READING_ENTRY = "delete_own_reading_entry"


# Role-to-permission mapping
ROLE_PERMISSIONS: Dict[RoleType, Set[Permission]] = {
    RoleType.STANDARD_USER: {
        # Standard users can view profiles
        Permission.VIEW_USER_PROFILE,
        # Standard users can manage books
        Permission.CREATE_BOOK,
        Permission.VIEW_BOOK,
        Permission.EDIT_OWN_BOOK,
        Permission.DELETE_OWN_BOOK,
        # Standard users can manage their own reading entries
        Permission.CREATE_READING_ENTRY,
        Permission.VIEW_READING_ENTRY,
        Permission.VIEW_OWN_READING_ENTRIES,
        Permission.EDIT_OWN_READING_ENTRY,
        Permission.DELETE_OWN_READING_ENTRY,
    },
    RoleType.ADMIN: {
        # Admins have all user management permissions
        Permission.MANAGE_USERS,
        Permission.ACTIVATE_USER,
        Permission.DEACTIVATE_USER,
        Permission.VIEW_ALL_USERS,
        Permission.VIEW_USER_PROFILE,
        # Admins have full control over books
        Permission.CREATE_BOOK,
        Permission.VIEW_BOOK,
        Permission.EDIT_BOOK,
        Permission.EDIT_OWN_BOOK,
        Permission.DELETE_BOOK,
        Permission.DELETE_OWN_BOOK,
        # Admins have full control over all reading entries
        Permission.CREATE_READING_ENTRY,
        Permission.VIEW_READING_ENTRY,
        Permission.VIEW_OWN_READING_ENTRIES,
        Permission.EDIT_READING_ENTRY,
        Permission.EDIT_OWN_READING_ENTRY,
        Permission.DELETE_READING_ENTRY,
        Permission.DELETE_OWN_READING_ENTRY,
    },
}


def user_has_permission(role: RoleType, permission: Permission) -> bool:
    return permission in ROLE_PERMISSIONS.get(role, set())


def get_role_permissions(role: RoleType) -> Set[Permission]:
    return ROLE_PERMISSIONS.get(role, set())
