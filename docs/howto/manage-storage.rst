.. _manage-storage:

How to manage storage
=====================


> See also: :ref:`juju:storage`

This document shows how to manage storage. This will enable you to allocate resources at a granular level and can be useful in optimizing the deployment of an application. The level of sophistication is limited by your cloud (whether it supports dynamic storage or storage configuration attributes),  and by the charm in charge of that application (whether it supports storage persistence, additional cache, etc.).


Add storage
-----------

To create and attach a storage instance to a unit, on a Unit object, use the `add_storage()` method, passing the storage name as an argument. For example:

.. code:: python

   await my_unit.add_storage("pgdata", size=512)


To attach an existing storage to an application during deployment, on a connected Model object, use the `attach_storage` parameter of the `deploy()` method.

.. code:: python

   await model.deploy('postgresql', attach_storage=[tag.storage("my-storage")])


> See more: `add_storage() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.unit.html#juju.unit.Unit.add_storage>`_, `Unit (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/unit.html>`_, `deploy() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.deploy>`_, `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_

List  available storage
-----------------------

To list available storage instances, on a connected Model object, use the `list_storage()` method. For example:

.. code:: python

   await model.list_storage()

> See more: `list_storage() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.list_storage>`_, `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_



Detach storage
--------------

To detach a storage instance from a unit, on a Unit object, use the `detach_storage()` method, passing the storage id as an argument. For example:

.. code:: python

   await my_unit.detach_storage("osd-devices/2")

> See more: `detach_storage() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.unit.html#juju.unit.Unit.detach_storage>`_, `Unit (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/unit.html>`_


Attach storage
--------------

To attach an existing storage instance to a unit, on a Unit object, use the `attach_storage()` method, passing the storage id as an argument. For example:

.. code:: python

   await my_unit.attach_storage(["osd-devices/2"])

> See more: `attach_storage() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.unit.html#juju.unit.Unit.attach_storage>`_, `Unit (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/unit.html>`_


Remove storage
--------------
> See also: :ref:`juju-removing-things`

To remove a storage instance, on a connected Model object, use the `remove_storage()` method, passing the storage id as an argument. For example:

.. code:: python

   # use force=True to remove storage even if it is currently attached
   await my_model.remove_storage(["osd-devices/2"], force=True)


> See more: `remove_storage() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.remove_storage>`_, `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_
