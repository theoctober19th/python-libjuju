.. _manage-controllers:

How to manage controllers
=========================

> See also: :ref:`juju:controller`


This document demonstrates various ways in which you can interact with a controller.



Bootstrap a controller
----------------------

> See also: :ref:`juju:list-of-supported-clouds`

With the `python-libjuju` client, you can only connect to a pre-existing controller. To bootstrap a controller, see the `juju` client.


View details about a controller
-------------------------------

To view details about a controller in `python-libjuju`, with a connected controller object (below, `controller`), you can call the `Controller.info()` function to retrieve information about the connected controller:

.. code:: python

   await controller.info()

> See more: `Controller.info() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.controller.html#juju.controller.Controller.info>`_


Switch to a different controller
--------------------------------

To switch to a different controller with `python-libjuju`, simply connect to the controller you want to work with, which is done by calling `connect` on the `Controller <https://pythonlibjuju.readthedocs.io/en/latest/narrative/controller.html>`_ object (below, `controller`):

.. code:: python

   from juju.model import Controller

   controller = Controller()
   await controller.connect() # will connect to the "current" controller

   await controller.connect('mycontroller') # will connect to the controller named "mycontroller"


Note that if the `controller` object is already connected to a controller, then that connection will be closed before making the new connection.

> See more:  `Controller.connect() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.connect>`_, `Connect with Authentication <https://pythonlibjuju.readthedocs.io/en/latest/narrative/controller.html#connecting-with-authentication>`_, `Connect with explicit endpoints <https://pythonlibjuju.readthedocs.io/en/latest/narrative/controller.html#connecting-with-an-explicit-endpoint>`_
