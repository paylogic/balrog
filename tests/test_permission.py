"""Permission related tests."""


def test_create(permission, permission_name):
    """Test permission creation."""
    assert permission.name == permission_name


def test_check(permission, identity):
    """Test Permission.check is True by default."""
    assert permission.check(identity)


def test_filter(permission, identity, objects):
    """Test Permission.check is True by default."""
    assert permission.filter(identity, objects) == objects
