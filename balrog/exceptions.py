"""Access control exceptions."""


class Error(Exception):

    """Base exception class.

    All errors extend this class which is useful to dispatch in error handlers.
    """


class PermissionNotFound(Error):

    """Permission is not found.

    Can't filter objects because there's no permission that implements filtering.
    """


class RoleNotFound(Error):

    """Role is not found.

    Role is not found for the name returned by the get_role callback.
    """
