"""Access control role."""

from balrog import exceptions


class Role(object):

    """Role, a set of permissions that identity can have access to."""

    def __init__(self, name, permissions):
        """Create a role.

        :param name: Unique role name within one policy.
        :param permissions: Permissions of the role.
        """
        self.name = name
        self.permissions = {}

        for permission in permissions:
            assert permission.name not in self.permissions, (
                'The permission `{0}` is already registered within this role.'.format(permission.name)
            )
            self.permissions[permission.name] = permission

    def check(self, identity, permission, *args, **kwargs):
        """Check if the identity has requested permission.

        :param identity: Currently authenticated identity.
        :param permission: Permission name.

        :return: True if identity role has this permission.
        """
        try:
            permission = self.permissions[permission]
        except KeyError:
            return False
        else:
            return permission.check(identity, *args, **kwargs)

    def filter(self, identity, permission, objects, *args, **kwargs):
        """Filter objects according to the permission this identity has.

        :param identity: Currently authenticated identity.
        :param permission: Permission name.
        :param objects: Objects to filter out.

        :returns: Filtered objects.
        :raises: `PermissionNotFound` when no permission is found that can
            filter the objects.
        """
        try:
            permission = self.permissions[permission]
        except KeyError:
            raise exceptions.PermissionNotFound()
        else:
            return permission.filter(identity, objects, *args, **kwargs)
