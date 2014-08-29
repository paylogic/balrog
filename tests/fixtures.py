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
def identity():
    """Identity object."""
    return User()


@pytest.fixture
def objects():
    """Objects to filter."""
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
