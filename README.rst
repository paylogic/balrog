Balrog
======

Balrog is a Python library that helps you to build an authorization system in your projects:

::

    You shall not pass!


Balrog is good for systems with statically defined roles that enable certain workflows.
Every identity can have only one role on the certain context. This approach allows covering
your system with functional tests according to the roles and flows these roles perform.
Formal requirements can be applied to the workflows in the system which will define roles.

These roles are statically defined in the code and this way properly versioned and covered
with testing. It is possible to do a composition of certain permission groups and share them
between roles, but semantically there's no way for one identity to have 2 contradicting
roles when one role forbids actions and the other allows them. Instead a proper role
can be extracted with the permissions it allows.


Installation
------------

.. code-block:: sh

    pip install balrog


Usage
-----

Permission is needed to access a resource or to perform an action. Permissions are grouped in the roles
and roles are grouped in the policies.

The entry point where a permission is being checked is the Policy. Define an instance of the Policy
and specify the list of roles it works with.

Project can contain multiple policies that serve different purposes.

Permission declaration:

.. code-block:: python


    import balrog
    from flask import request

    def get_identity(*args, **kwargs):
    """Get current user."""
        # Flask request wrapper implements the ``user`` property
        return request.user

    def get_role(identity, *args, **kwargs):
    """Get current identity role."""
        # User.role is a property of the ORM User model
        return identity.role


    read = balrog.Permissions(name="article.read")
    post = balrog.Permissions(name="article.post")
    comment = balrog.Permissions(name="article.comment")

    anonymous = balrog.Role(
        name="anonymous",
        permissions=[read],
    )
    """Anonymous visitors can read articles."""

    user = balrog.Role(
        name="user",
        permissions=[read, comment],
    )
    """User accounts can read and comment articles."""

    author = balrog.Role(
        name="author",
        permissions=[read, post, comment],
    )
    """Author accounts can read, create and comment articles."""

    policy = balrog.Policy(
        roles=[anonymous, user, author],
        get_identity=get_identity,
        get_role=get_role,
        permissions=[read, post, comment]
    )


Permission checking:

.. code-block:: python

    # ...
    policy = balrog.Policy(roles=[anonymous, user, author], get_identity=get_identity, get_role=get_role)
    policy.check("article.comment")


Filtering collections:

.. code-block:: python

    articles = session.query(Article)
    my_articles = policy.filter("article.view", objects=articles)


Every role is a collection of permissions. Besides being included in the role permissions can
implement even more detailed checking and filtering logic.


Permission
----------

Permissions have unique names (within the role) which reflect the resource and the action you
want to take with this resource.

.. code-block:: python

    import balrog

    eat = balrog.Permission(name="cucumber.eat")
    happy = balrog.Permission(name="be-happy")


Name is just a string identifier that you are using in order to ask a policy for a permission.
The name formatting convention can be decided per project.

Permissions have 2 methods: ``check`` and ``filter``. By default the ``check`` method implements ``True``
and the ``filter`` method is simply bypassing the objects. These methods are an additional opportunities
to control the access to certain context, instances of your resources, check whitelists, filter out objects
from collections that can not be seen by currently authenticated identity, etc.


Role
----

Roles have unique names within the policy. Role name is determined by the authenticated identity
and used in the policy permission check implicitly.

Roles are collections of permissions that define the role and enable certain workflows in your
system.

When a system is large and has a lot of specific permissions declared sometimes it is easier to
subclass the Role class instead of granting all permissions to the role:

.. code-block:: python

    import balrog


    class Admin(balrog.Role):

        def check(self, identity, permission, *args, **kwargs):
            return True



Policy
------

Policy is used as an entry point of permission checking in your project. It incapsulates the roles
that define your workflows. There could be multiple policy instances in the project.

Besides roles policy requires some configuration and backend implementation:

get_identity
~~~~~~~~~~~~

A callback that returns currenlty authenticated identity. Projects have to implement this backend
and restore the identity instance (e.g. User object) for example from the Flask Request object.

.. code-block:: python

    from flask import request

    def get_identity(*args, **kwargs):
    """Get current user."""
        # Flask request wrapper implements the ``user`` property
        return request.user



get_role
~~~~~~~~

A callback that returns which role current identity has on the context. In the simple case the role is associated
to the user in the database.


.. code-block:: python

    def get_role(identity, *args, **kwargs):
    """Get current identity role."""
        # User.role is a property of the ORM User model
        return identity.role


check
~~~~~

The permission check. All arguments that you pass to this function are passed along in Role.check and finally
to Permission.check.

.. code-block:: python

    if not policy.check("article.read", article=a):
        flask.abort("You can't access the article `{0}`".format(a.id))

filter
~~~~~~

The function that is filtering out items of the given objects if the identity has no permission to access them.


.. code-block:: python

    articles = session.query(Article).filter_by(is_published=True)

    my_articles = policy.filter("article.read", objects=articles)


Implementing your own filtering:

.. code-block:: python

    import balrog

    class ViewArticle(balrog.Permission);

        def filter(self, identity, objects, *args, **kwargs):
            """Filter out articles of the other users.

            :param identity: User object.
            :param objects: SQLAlchemy query.

            :returns: SQLAlchemy query with applied filtering.
            """
            return objects.filter_by(user_id=identity.id)


Filter function can raise an exception in the case when there's no such permission
in the role of the identity. In this case the library doesn't know for sure what type to
return that represents an empty collection of objects. Some projects would expect
an empty list, some - falsy ORM query, etc. Instead the exception should be handled:


.. code-block:: python

    try:
        my_articles = policy.filter("article.read", objects=articles)
    except balrog.PermissionNotFound:
        my_articles = []


context
~~~~~~~

Everything that you pass extra to the check or filter function is passed along to the regarding
Role and Permission methods.
You can pass certain instance of an object you control your access using whitelists.

.. code-block:: python

    policy.check("message.send", ip=ip_addr)


Policy.check method can compare if ip address is in a whitelist.


Contact
-------

If you have questions, bug reports, suggestions, etc. please create an issue on
the `GitHub project page <http://github.com/paylogic/balrog>`_.


License
-------

This software is licensed under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_

See `License <https://github.com/paylogic/balrog/blob/master/LICENSE.txt>`_