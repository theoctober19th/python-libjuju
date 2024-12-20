.. _manage-charm-resources:

How to manage charm resources
=============================

> See also: :ref:`juju:resource-charm`

When you deploy / update an application from a charm, that automatically deploys / updates any charm resources, using the defaults specified by the charm author. However, you can also specify resources manually (e.g., to try a resource released only to `edge` or to specify a non-Charmhub resource). This document shows you how.


Find out the resources available for a charm
--------------------------------------------

To find out what resources are available for a charm on Charmhub, on a connected Model object, select the `charmhub` object associated with the model, and use the `list_resources()` method, passing the name of the charm as an argument. For example:

.. code:: python

   await model.charmhub.list_resources('postgresql-k8s')

> See more: `charmhub (property) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.charmhub>`_, `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_

Specify the resources to be deployed with a charm
-------------------------------------------------

To specify a resource during deployment, on a connected Model object, use the `deploy` method, passing the resources as a parameter. For example:

.. code:: python

   resources = {"file-res": "test.file"}
   app = await model.deploy(charm_path, resources=resources)

To update a resource after deployment by uploading file from local disk, on an Application object, use the `attach_resource()` method, passing resource name, file name and the file object as parameters.

.. code:: python

   with open(str(charm_path / 'test.file')) as f:
       app.attach_resource('file-res', 'test.file', f)



> See more: `deploy() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.deploy>`_, `attach_resource() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.application.html#juju.application.Application.attach_resource>`_, `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_

View the resources deployed with a charm
----------------------------------------

To view the resources that have been deployed with a charm, on an Application object, use the `get_resources()` method. For example:

.. code:: python

   await my_app.get_resources()

> See more: `get_resources() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.application.html#juju.application.Application.get_resources>`_, `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_
