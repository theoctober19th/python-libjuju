.. _manage-units:

How to manage units
===================

> See also: :ref:`juju:unit`

Add a unit
----------

To add a unit in `python-libjuju` client, you simply call `add_unit()` on your `Application` object, as follows:

.. code:: python

   my_app.add_unit(count=3)

> See more: `Application (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/application.html>`_, `Application.add_unit() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.application.html#juju.application.Application.add_unit>`_, `Application.scale() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.application.html#juju.application.Application.scale>`_

.. _control-the-number-of-units:
Control the number of units
---------------------------

To control the number of units of an application in `python-libjuju` client, you can use the `Application.add_unit()` and `Application.destroy_units()` methods, or the `Application.scale()` method, depending on whether you're working on a CAAS system (e.g. Kubernetes), or an IAAS system (e.g. lxd).

If you're on  an IAAS system (machine applications):

.. code:: python

   u = my_app.add_unit()
   my_app.destroy_units(u.name) # Note that the argument is the name of the unit

   # You may give multiple unit names to destroy at once
   my_app.destroy_units(u1.name, u2.name)


   If you're on  a CAAS system (k8s applications):

.. code:: python

   my_app.scale(4)


> See more: `Application (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/application.html>`_, `Application.add_unit() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.application.html#juju.application.Application.add_unit>`_, `Application.scale() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.application.html#juju.application.Application.scale>`_, `Application.destroy_units() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.application.html#juju.application.Application.destroy_units>`_


Show details about a unit
-------------------------

To see details about a unit in `python-libjuju` client, you can use various fields and methods of a `Unit` object. For example, to get the `public_address` of a unit:

.. code:: python

   my_unit.get_public_address()

Or, to see if the unit is a leader:

.. code:: python

   my_unit.is_leader_from_status()

> See more: `Unit (methods) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.unit.html#juju.unit.Unit>`_, `Unit.get_public_address() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.unit.html#juju.unit.Unit.get_public_address>`_, `Unit.is_leader_from_status() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.unit.html#juju.unit.Unit.is_leader_from_status>`_


Show the status of a unit
-------------------------

To get the status of a unit on `pylibjuju-client`, you can use various (dynamically updated) status fields defined on a Unit object, such as:

.. code:: python

   workload_st = my_unit.workload_status
   agent_st = my_unit.agent_status

> See more: `Unit status <https://juju.is/docs/juju/status#heading--unit-status>`_, `Unit (methods) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.unit.html#juju.unit.Unit>`_, `Unit.workload_status (field) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.unit.html#juju.unit.Unit.workload_status>`_, `Unit.agent_status (field) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.unit.html#juju.unit.Unit.agent_status>`_


Mark unit errors as resolved
----------------------------

To mark unit errors as resolved in the `python-libjuju` client, you can call the `resolved()` method on a `Unit` object:

.. code:: python

   await my_unit.resolved()

> See more: `Unit.resolved() https://pythonlibjuju.readthedocs.io/en/latest/api/juju.unit.html#juju.unit.Unit.resolved`_


Remove a unit
-------------

To remove individual units on `python-libjuju` client, simply use the `Application.destroy_units()` method:


.. code:: python

   my_app.destroy_units(u.name) # Note that the argument is the name of the unit

   # You may give multiple unit names to destroy at once
   my_app.destroy_units(u1.name, u2.name)

> See more: `Application (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/application.html>`_, `Application.destroy_units() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.application.html#juju.application.Application.destroy_units>`_
