"""Access control permission."""


class Permission(object):

    """Permission that identity can have."""

    def __init__(self, name):
        """Create permission.

        :param name: Unique permission name within one role.
        """
        self.name = name

    def check(self, identity, *args, **kwargs):
        """Check if permission applies to this identity.

        :param identity: Currently authenticated identity.

        :return: `True` if permission is granted to requested identity.
        :note: This function could be overridden in order to do additional check
            in the certain context.
        """
        return True

    def filter(self, identity, objects, *args, **kwargs):
        """Filter objects according to this permission and identity.

        :param identity: Currently authenticated identity.
        :param objects: Objects to filter out.

        :returns: Filtered objects.
        :note: This function should be overridden in order to implement the
            filtering in the certain context.
        """
        return objects
