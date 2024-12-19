.. _manage-secrets:

How to manage secrets
=====================

> See also: :ref:`juju:secret`

Charms can use relations to share secrets, such as API keys, a database’s address, credentials and so on. This document demonstrates how to interact with them as a Juju user.


Add a secret
------------

To add a (user) secret, on a connected Model, use the `add_secret()` method, passing the name of the secret and the data as arguments. For example:

.. code:: python

   await model.add_secret(name='my-apitoken', data_args=['token=34ae35facd4'])

> See more: `add_secret() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.add_secret>`_, `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_


View all the available secrets
------------------------------

To view all the (user and charm) secrets available in a model, on a connected Model, use the `list_secrets()` method.

.. code:: python

   await model.list_secrets()

> See more: `list_secrets() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.list_secrets>`_, `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_



Grant access to a secret
------------------------

Given a model that contains both your (user) secret and the application(s) that you want to grant access to, to grant the application(s) access to the secret, on a connected Model, use the `grant_secret()` method, passing the name of the secret and the application name as arguments. For example:

.. code:: python

   await model.grant_secret('my-apitoken', 'ubuntu')

Similarly, you can use the `revoke_secret()` method to revoke access to a secret for an application.

.. code:: python

   await model.revoke_secret('my-apitoken', 'ubuntu')

> See more: `grant_secret() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.grant_secret>`_, `revoke_secret() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.revoke_secret>`_, `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_


Update a secret
---------------
> *This feature is opt-in because Juju automatically removing secret content might result in data loss.*

To update a (user) secret, on a connected Model, use the `update_secret()` method, passing the name of the secret and the updated info arguments. You may pass in `data_args`, `new_name`, `file` and `info` to update the secret (check out the documentation for details). For example:

.. code:: python

   await model.update_secret(name='my-apitoken', new_name='new-token')

> See more: `update_secret() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.update_secret>`_, `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_


Remove a secret
---------------

To remove a secret from a model, on a connected Model, use the `remove_secret()` method, passing the name of the secret as an argument. For example:

.. code:: python

   # Remove all the revisions of a secret
   await model.remove_secret('my-apitoken')

   # Remove the revision 2 of a secret
   await model.remove_secret('my-apitoken', revision=2)

> See more: `remove_secret() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.remove_secret>`_, `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_
