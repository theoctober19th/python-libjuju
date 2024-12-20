.. _manage-spaces:

How to manage spaces
====================

> See also: :ref:`juju:space`


Add a space
-----------

To create and add a new space, on a connected Model object, use the `add_space()` method, passing a name for the space and associated subnets. For example:

.. code:: python

  await my_model.add_space("db-space", ["172.31.0.0/20"])

> See more: `add_space() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.add_space>`_, `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_



View  available spaces
----------------------

To view available spaces, on a connected Model, use the `get_spaces()` method.

.. code:: python

   await my_model.get_spaces()

> See more: `get_spaces() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.get_spaces>`_, `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_
