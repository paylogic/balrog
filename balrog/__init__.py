"""Balrog public API."""

__version__ = '1.1.0'

try:
    from balrog.policy import Policy
    from balrog.role import Role
    from balrog.permission import Permission
    from balrog.exceptions import Error, PermissionNotFound, RoleNotFound

    __all__ = ['Policy', 'Role', 'Permission', 'Error', 'PermissionNotFound', 'RoleNotFound']
except ImportError:
    # avoid import errors when only __version__ is needed (for setup.py)
    pass
