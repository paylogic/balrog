"""Role related tests."""

import pytest
import mock
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


def test_check(role, identity, permission_name):
    """Test Role.check."""
    with mock.patch.object(balrog.Permission, 'check') as mock_check:
        mock_check.return_value = True
        assert role.check(identity, permission_name, 1, 2, 3, a=1, b=2, c=3)
        mock_check.assert_called_once_with(identity, 1, 2, 3, a=1, b=2, c=3)


@pytest.mark.parametrize(
    'name',
    (
        'unknown',
        None,
        -1,
    ),
)
def test_check_permission_not_found(role, identity, permission_name, name):
    """Test Role.check is False when permission is not found."""
    assert name != permission_name
    assert not role.check(identity, name)


def test_filter(role, identity, permission_name, objects):
    """Test Role.filter bypasses the objects by default."""

    with mock.patch.object(balrog.Permission, 'filter') as mock_filter:
        mock_filter.return_value = objects
        # None is passed here for default explicitly in order the call args to match
        assert role.filter(identity, permission_name, objects, None, 1, 2, 3, a=1, b=2, c=3) == objects
        mock_filter.assert_called_once_with(identity, objects, 1, 2, 3, a=1, b=2, c=3)


def test_filter_without_permission(role, identity, permission_name, objects):
    """Test Role.filter returns empty list when not allowed."""
    assert role.filter(identity, 'unknown', objects) == []


def test_filter_without_permission_default(role, identity, permission_name, objects):
    """Test Role.filter returns the result of default when not allowed."""
    default = lambda objects: ['d', 'e', 'f', 'a', 'u', 'l', 't']
    assert role.filter(identity, 'unknown', objects, default=default) == ['d', 'e', 'f', 'a', 'u', 'l', 't']
