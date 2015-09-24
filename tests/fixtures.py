"""Common fixtures."""

import pytest
import balrog


class User(object):

    """Test identity."""

    name = 'user'


@pytest.fixture
def permission_name():
    """Permission name."""
    return 'test-balrog'


@pytest.fixture
def permission(permission_name):
    """Permission object."""
    return balrog.Permission(name=permission_name)


@pytest.fixture
def identity(identity_role):
    """Identity object."""
    user = User()
    user.role = identity_role
    return user


@pytest.fixture
def objects():
    """The objects to filter."""
    return [1, 2, 3]


@pytest.fixture
def role_name():
    """Role name."""
    return 'test-role'


@pytest.fixture
def role_permissions(permission):
    """Role permissions."""
    return [permission]


@pytest.fixture
def role(role_name, role_permissions):
    """Role object."""
    return balrog.Role(name=role_name, permissions=role_permissions)


@pytest.fixture
def identity_role(role):
    """The role to use for the identity."""
    return role


@pytest.fixture
def policy_roles(role):
    """Policy roles."""
    return [role]


@pytest.fixture
def get_identity(identity):
    """Get identity policy callback."""
    def _get_identity(*args, **kwargs):
        return identity
    return _get_identity


@pytest.fixture
def get_role():
    """Get role policy callback."""
    def _get_role(identity, *args, **kwargs):
        try:
            return identity.role.name
        except AttributeError:
            return
    return _get_role


@pytest.fixture
def policy(policy_roles, get_identity, get_role):
    """Role object."""
    return balrog.Policy(
        roles=policy_roles,
        get_identity=get_identity,
        get_role=get_role
    )
