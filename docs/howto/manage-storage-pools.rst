.. _manage-storage-pools:

How to manage storage pools
===========================

> See also: :ref:`juju:storage-pool`

Create a storage pool
---------------------

To create a storage pool, on a connected Model object, use the `create_storage_pool()` method, passing the name of the pool and the provider type. For example:

.. code:: python

   await my_model.create_storage_pool("test-pool", "lxd")

> See more: `create_storage_pool() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.create_storage_pool>`_, `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_


View the available storage pools
--------------------------------

To view the available storage pools, on a connected Model object, use the `list_storage_pools()` method. For example:

.. code:: python

   await my_model.list_storage_pools()

> See more: `list_storage_pools() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.list_storage_pools>`_, `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_


Update a storage pool
---------------------

To update an existing storage pool attributes, on a connected Model object, use the `update_storage_pool()` method, passing the name of the storage and the attribute values to update. For example:

.. code:: python

   await my_model.update_storage_pool(
       "operator-storage",
       attributes={"volume-type": "provisioned-iops", "iops": "40"})

> See more: `update_storage_pool() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.update_storage_pool>`_, `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_


Remove a storage pool
---------------------

To remove a storage pool, on a connected Model object, use the `remove_storage_pool()` method, passing the name of the storage. For example:

.. code:: python

   await my_model.remove_storage_pool("test-pool")

> See more: `remove_storage_pool() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.remove_storage_pool>`_, `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_
