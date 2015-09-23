"""Access control policy."""

from balrog import exceptions


class Policy(object):

    """Controls the access of a certain actor to a certain action on a resource."""

    def __init__(self, roles, get_identity, get_role):
        """Create and configure access control.

        :param roles: All roles of this access control.
        :param get_identity: Callable that returns the currently authenticated
            identity.
        :param get_role: Callable that returns role name of the currently authenticated
            identity.
        """
        self._get_identity = get_identity
        self._get_role = get_role
        self.roles = {}

        for role in roles:
            assert role.name not in self.roles, (
                u'The role `{0}` is already registered.'.format(role.name)
            )
            self.roles[role.name] = role

    def get_identity(self, *args, **kwargs):
        """Get current identity.

        :returns: An identity object which can be provided via a callback.
        """
        return self._get_identity(*args, **kwargs)

    def get_role(self, identity, *args, **kwargs):
        """Get identity role.

        :returns: Identity role object which name can be provided via a callback.
        :raises: `RoleNotFound` if no role found for this identity.
        """
        name = self._get_role(identity, *args, **kwargs)

        try:
            return self.roles[name]
        except KeyError:
            raise exceptions.RoleNotFound(name)

    def check(self, permission, *args, **kwargs):
        """Check if the identity has requested permission.

        :param permission: Permission name.
        :return: `True` if identity role has this permission.
        """
        identity = self.get_identity(*args, **kwargs)
        role = self.get_role(identity, *args, **kwargs)
        if role is None:
            return False
        return role.check(identity, permission, *args, **kwargs)

    def filter(self, permission, objects, *args, **kwargs):
        """Filter objects according to the permission this identity has.

        :param permission: Permission name.
        :param objects: Objects to filter out.
        :returns: Filtered objects.
        :raises: `RoleNotFound` if no role found for this identity.
        :raises: `PermissionNotFound` when no permission is found that can
            filter the objects.
        """
        identity = self.get_identity(*args, **kwargs)
        role = self.get_role(identity, *args, **kwargs)
        return role.filter(identity, permission, objects, *args, **kwargs)
