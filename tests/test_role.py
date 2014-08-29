"""Role related tests."""

import pytest
import balrog


def test_create(role, role_name, role_permissions):
    """Test role creation."""
    assert role.name == role_name
    assert role.permissions == dict((perm.name, perm) for perm in role_permissions)


def test_permission_name_is_unique(role_name, permission):
    """Test that permissions are registered with unique name."""
    with pytest.raises(AssertionError):
        balrog.Role(
            name=role_name,
            permissions=(
                permission,
                permission,
            ),
        )
