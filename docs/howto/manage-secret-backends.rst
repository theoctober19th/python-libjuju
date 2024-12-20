.. _manage-secret-backends:

How to manage secret backends
=============================

> See also: :ref:`juju:secret-backend`


Starting with Juju `3.1.0`, you can also manage secret backends in a number of ways.


Add a secret backend to a model
-------------------------------

To add a secret backend to a controller, on a connected Controller, use the `add_secret_backends()` method, passing the `id`, `name`, `backend_type`, and `config` as arguments. For example:

.. code:: python

   await my_controller.add_secret_backends("1001", "myvault", "vault", {"endpoint": vault_url, "token": keys["root_token"]})

> See more: `add_secret_backends() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.controller.html#juju.controller.Controller.add_secret_backends>`_, `Controller (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/controller.html>`_


View all the secret backends available on a controller
------------------------------------------------------

To view all the secret backends available in the controller, on a connected Controller, use the `list_secret_backends()` method.

.. code:: python

   list = await my_controller.list_secret_backends()

> See more: `list_secret_backends() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.controller.html#juju.controller.Controller.list_secret_backends>`_, `Controller (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/controller.html>`_


Update a secret backend
-----------------------

To update a secret backend on the controller, on a connected Controller, use the `update_secret_backends()` method, passing the backend name as argument, along with the updated information, such as `name_change` for a new name. For example:

.. code:: python

   await my_controller.update_secret_backends(
               "myvault",
               name_change="changed_name")

Check out the documentation for the full list of arguments.

> See more: `update_secret_backends() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.controller.html#juju.controller.Controller.update_secret_backends>`_, `Controller (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/controller.html>`_

Remove a secret backend
-----------------------

To remove a secret backend on the controller, on a connected Controller, use the `remove_secret_backends()` method, passing the backend name as argument. For example:

.. code:: python

   await my_controller.remove_secret_backends("myvault")

Check out the documentation for the full list of arguments.

> See more: `remove_secret_backend() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.controller.html#juju.controller.Controller.remove_secret_backends>`_, `Controller (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/controller.html>`_
