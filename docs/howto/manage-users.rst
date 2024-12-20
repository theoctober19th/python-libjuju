.. _manage-users:


How to manage users
===================

> See also: :ref:`juju:user`


Add a user
----------


To add a user to a controller, on a connected Controller object, use the `add_user()` method.

.. code:: python

   await my_controller.add_user("alex")

> See more: `add_user() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.controller.html#juju.controller.Controller.add_user>`_


List all the known users
------------------------

To view a list of all the users known (i.e., allowed to log in) to a controller, on a connected Controller object, use the `get_users()` method.

.. code:: python

   await my_controller.get_users()

> See more: `get_users() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.controller.html#juju.controller.Controller.get_users>`_


View details about a user
-------------------------

To view details about a specific user, on a connected Controller, use the `get_user()` method to retrieve a User object that encapsulates everything about that user. Using that object, you can access all the details (via the object properties) for that user.

.. code:: python

   user_object = await my_controller.get_user("alice")
   # Then we can access all the properties to view details
   print(user_object.display_name)
   print(user_object.access)
   print(user_object.date_created)
   print(user_object.last_connection)

> See more: `get_user() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.controller.html#juju.controller.Controller.get_user>`_, `User (module) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.user.html#juju.user.User>`_


View details about the current user
-----------------------------------

To see details about the current user, on a connected Controller, use the `get_current_user()` method to retrieve a User object that encapsulates everything about the current user. Using that object, you can access all the details (via the object properties) for that user.

.. code:: python

   user_object = await my_controller.get_current_user()
   # Then we can access all the properties to view details
   print(user_object.display_name)
   print(user_object.access)
   print(user_object.date_created)
   print(user_object.last_connection)

> See more: `get_current_user() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.controller.html#juju.controller.Controller.get_current_user>`_, `User (module) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.user.html#juju.user.User>`_


Manage a user's access level
----------------------------
> See also: :ref:`juju:user-access-levels`

To manage a user's access to a controller, a model, or an offer, on a User object, use the `grant()` and `revoke()` methods to grant or revoke a certain access level to a user.

.. code:: python

   # grant a superuser access to the controller (that the user is on)
   await user_object.grant('superuser')

   # grant user the access to see a model
   await user_object.grant("read", model_name="test-model")

   # revoke ‘read’ (and ‘write’) access from user for application offer ‘fred/prod.hosted-mysql’:
   await user_object.revoke("read", offer_url="fred/prod.hosted-mysql")

> See more: `grant() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.user.html#juju.user.User.grant>`_,  `revoke() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.user.html#juju.user.User.revoke>`_, `User (module) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.user.html#juju.user.User>`_


Manager a user's login details
------------------------------

To set or change a user's password, on a User object, use the `set_password()` method.

.. code:: python

   await user_object.set_password('123')


> See more: `set_password() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.user.html#juju.user.User.set_password>`_, `User (module) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.user.html#juju.user.User>`_

Manage a user's enabled status
------------------------------

To enable or disable a user, on a User object, use the `enable()` and `disable()` methods.

.. code:: python

   await user_object.enable()

   await user_object.disable()

You can also check if a user is enabled or disabled using the `enabled` and `disabled` properties on the User object.

.. code:: python

   # re-enable a disabled user
   if user_object.disabled:
       await user_object.enable()


> See more: `enable() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.user.html#juju.user.User.enable>`_, `disable() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.user.html#juju.user.User.disable>`_, `User (module)  <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.user.html#juju.user.User>`_


Remove a user
-------------

To remove a user, on a connected Controller object, use the `remove_user()` method.

.. code:: python

   await my_controller.remove_user("bob")


> See more: `remove_user() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.controller.html#juju.controller.Controller.remove_user>`_, `User (module) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.user.html#juju.user.User>`_
