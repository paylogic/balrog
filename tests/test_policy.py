"""Policy related tests."""

import pytest
import mock
import balrog


@pytest.mark.parametrize(
    'all_permissions',
    (
        None,
        ['test'],
        ['test1', 'test2'],
    )
)
def test_create(policy, policy_roles, all_permissions):
    """Test policy creation."""
    assert policy.roles == dict((role.name, role) for role in policy_roles)
    if all_permissions is None:
        assert policy.permissions is None
    else:
        for permission in all_permissions:
            assert permission in policy.permissions


def test_role_name_is_unique(role, get_role, get_identity):
    """Test that roles are registered with unique name."""
    with pytest.raises(AssertionError):
        balrog.Policy(
            roles=(
                role,
                role,
            ),
            get_role=get_role,
            get_identity=get_identity,
        )


def test_check(policy, permission_name, identity):
    """Test Policy.check."""
    with mock.patch.object(balrog.Role, 'check') as mock_check:
        mock_check.return_value = True
        assert policy.check(permission_name, 1, 2, 3, a=1, b=2, c=3)
        mock_check.assert_called_once_with(identity, permission_name, 1, 2, 3, a=1, b=2, c=3)


@pytest.mark.parametrize(
    'name',
    (
        'unknown',
        None,
        -1,
    ),
)
def test_check_permission_not_found(policy, permission_name, name):
    """Test Policy.check is False when permission is not found."""
    assert name != permission_name
    assert not policy.check(name)

@pytest.mark.parametrize(
    'identity_role',
    (
        None,
    )
)
def test_check_role_not_found(policy, permission_name, identity_role):
    """Test Policy.check is False when role is not found."""
    assert not policy.check(permission_name)



def test_filter(policy, identity, permission_name, objects):
    """Test Policy.filter bypasses the objects by default."""
    with mock.patch.object(balrog.Role, 'filter') as mock_filter:
        mock_filter.return_value = objects
        # None is passed here for default explicitly in order the call args to match
        assert policy.filter(permission_name, objects, 1, 2, 3, a=1, b=2, c=3) == objects
        mock_filter.assert_called_once_with(identity, permission_name, objects, 1, 2, 3, a=1, b=2, c=3)


def test_filter_without_permission(policy, identity, permission_name, objects):
    """Test Policy.filter raises an exception when not allowed."""
    with pytest.raises(balrog.PermissionNotFound):
        policy.filter('unknown', objects)


def test_get_role(policy, identity):
    """Test get_role raises an exception for unknown role name."""
    with pytest.raises(balrog.RoleNotFound):
        with mock.patch.object(policy, '_get_role') as mock_get_role:
            mock_get_role.return_value = 'unknown'
            policy.get_role(identity)


@pytest.mark.parametrize(
    'all_permissions',
    (
        ['test1'],
    )
)
def test_check_with_permissions(policy, all_permissions, permission):
    """Test that if we specify no permissions on the policy the checks fails."""
    with pytest.raises(balrog.PermissionNotFound):
        policy.check(permission)
    assert not policy.check('test1')
