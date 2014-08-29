"""Access control policy."""


class Policy(object):

    """Controls the access of a certain actor to a certain action on a resource."""

    def __init__(self, roles, get_identity=None, get_role=None):
        """Create and configure access control.

        :param roles: All roles of this access control.
        :param get_role: Callable that returns role name of the currently authenticated
            identity.
        :param get_identity: Callable that returns role of the currently authenticated
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

    def get_identity(self):
        """Get current identity.

        :returns: Identity object which can be provided via a callback.
        """
        if self._get_identity:
            return self._get_identity()
        return None

    def get_role(self, identity, *args, **kwargs):
        """Get identity role.

        :returns: Identity role object which name can be provided via a callback.
        """
        if self._get_role:
            name = self._get_role(identity, *args, **kwargs)

            if name is None:
                return None

            assert (
                name in self.roles,
                u'Role `{0}` is not registered in this policy.'.format(name)
            )
            return self.roles[name]
        return None

    def check(self, permission, *args, **kwargs):
        """Check if the identity has requested permission.

        :param permission: Permission name.
        :return: `True` if identity role has this permission.
        """
        identity = self.get_identity()
        role = self.get_role(identity, *args, **kwargs)
        if role is None:
            return False
        return role.check(identity, permission, *args, **kwargs)

    def filter(self, permission, objects, default=None, *args, **kwargs):
        """Filter objects according to the permission this identity has.

        :param permission: Permission name.
        :param objects: Objects to filter out.
        :param default: Callable that makes falsy result from objects in the case
                        when no role is found. Defaults to empty list.
        :returns: Filtered objects.
        """
        identity = self.get_identity()
        role = self.get_role(identity, *args, **kwargs)
        if role is None:
            if callable(default):
                return default(objects)
            else:
                return []
        return role.filter(identity, permission, objects, default, *args, **kwargs)
