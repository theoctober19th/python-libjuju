.. _manage-models:

How to manage models
====================

> See also: :ref:`juju:model`

Add a model
-----------

To add a model, on a connected controller, call the `add_model` function. For example, below we're adding a model called `test-model` on the `controller`:

.. code:: python

   await controller.add_model("test-model")

> See more: `Controller.add_model() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.controller.html#juju.controller.Controller.add_model)>`_, `juju_model (module) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html>`_, `juju_controller (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/controller.html>`_


View all the models available on a controller
---------------------------------------------

To view all the models available on a controller, call the `Controller.list_models()` function:

.. code:: python

   await controller.list_models()

> See more: `Controller.list_models() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.controller.html#juju.controller.Controller.list_models>`_


Switch to a different model
---------------------------

In `python-libjuju`, switching to a different model means simply connecting to the model you want to work with, which is done by calling `connect` on the `Model <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_ object:

.. code:: python

   from juju.model import Model

   model = Model()
   await model.connect() # will connect to the "current" model

   await model.connect(model_name="test-model") # will connect to the model named "test-model"

Note that if the `model` object is already connected to a model, then that connection will be closed before making the new connection.

> See more:  `Model.connect() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.connect>`_


View the status of a model
--------------------------

TBA



View details about a model
--------------------------

TBA


Configure a model
-----------------
> See also: :ref:`juju:model-configuration`, :ref:`juju:list-of-model-configuration-keys`

TBA


Manage constraints for a model
------------------------------
> See also: :ref:`juju-constraint`

TBA


Destroy a model
---------------

To destroy a model, with a connected controller object, call the `Controller.destroy_model()` function. For example:

.. code:: python

   await controller.destroy_model("test-model")


> See more: `Controller.destroy_model() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.controller.html#juju.controller.Controller.destroy_model>`_
