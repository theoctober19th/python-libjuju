.. _manage-clouds:

How to manage clouds
====================

> See also: :ref:`juju:cloud`, :ref:`juju:list-of-supported-clouds`

This document shows how to manage your existing cloud(s) with Juju.


Add a cloud
-----------


With `python-libjuju`, you can only add a cloud definition to a controller you've already bootstrapped with the `juju` client.

To add a cloud, use the `Controller.add_cloud()` method on a connected `Controller` object. For example:

.. code:: python

   from juju.client import client as jujuclient

   await my_controller.add_cloud("my-cloud",
       jujuclient.Cloud(
               auth_types=["userpass"],
               endpoint="http://localhost:1234",
               type_="kubernetes",
       ))




> See more: `add_cloud (method) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.controller.html#juju.controller.Controller.add_cloud>`_, `Cloud (object) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.client.html#juju.client._definitions.Cloud>`_


View all the known clouds
-------------------------

To get all clouds known to the controller, you may use the `Controller.clouds()` method on a connected `Controller` object. It will return a list of Cloud objects.

.. code:: python

   await my_controller.clouds()

> See more: `clouds (method) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.controller.html#juju.controller.Controller.clouds>`_, `Cloud (object) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.client.html#juju.client._definitions.Cloud>`_


View details about a cloud
--------------------------

To get more detail about a particular cloud, you may use the `Controller.cloud()` method on a connected `Controller` object. It will return a Cloud object.

.. code:: python

   await my_controller.cloud()



> See more: `cloud (method) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.controller.html#juju.controller.Controller.cloud>`_, `Cloud (object) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.client.html#juju.client._definitions.Cloud>`_


Manage cloud credentials
------------------------
> See more: :ref:`manage-credentials`


Remove a cloud
--------------
> See also: :ref:`juju:removing-things`

To remove a cloud definition, you may use the `Controller.remove_cloud()` method on a connected `Controller` object.

.. code:: python

   await my_controller.remove_cloud()


> See more: `remove_cloud (method) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.controller.html#juju.controller.Controller.remove_cloud)>`_
