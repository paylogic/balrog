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
