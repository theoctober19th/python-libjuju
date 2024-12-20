.. _manage-applications:

How to manage applications
==========================

> See also: :ref:`juju:application`

Deploy an application
---------------------

To deploy an application, find and deploy a charm / bundle that delivers it.

> See more: :ref:`deploy-a-charm`

View details about an application
---------------------------------

To view details about an application on python-libjuju, you may use various `get_*` methods that are defined for applications.

For example, to get the config for an application, call `get_config()` method on an `Application` object:

.. code:: python

   config = await my_app.get_config()


> See more: `Application.get_config (method) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.application.html#juju.application.Application.get_config>`_, `Application (methods) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.application.html#juju.application.Application>`_


Trust an application with a credential
--------------------------------------

Some applications may require access to the backing cloud in order to fulfil their purpose (e.g., storage-related tasks). In such cases, the remote credential associated with the current model would need to be shared with the application. When the Juju administrator allows this to occur the application is said to be *trusted*.

To trust an application during deployment in python-libjuju, you may call the `Model.deploy()` with the `trust` parameter:

.. code:: python

   await my_model.deploy(..., trust=True, ...)

To trust an application after deployment, you may use the `Application.set_trusted()` method:

.. code:: python

   await my_app.set_trusted(True)


> See more: `Application.set_trusted (method) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.application.html#juju.application.Application.set_trusted>`_, `Application.get_trusted (method) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.application.html#juju.application.Application.get_trusted>`_


Run an application action
-------------------------

> See more: :ref:`manage-actions`

Configure an application
------------------------

**Get values.** To view the existing configuration for an application on python-libjuju, you may use the `Application.get_config()` method:

.. code:: python

   config = await my_app.get_config()


**Set values.** To set configuration values for an application on python-libjuju:

* To configure an application at deployment, simply provide a `config` map during the `Model.deploy()` call:

.. code:: python

   await my_model.deploy(..., config={'redirect-map':'https://demo'}, ...)


* To configure an application post deployment, you may use the `Application.set_config()` method, similar to passing config in the deploy call above:

.. code:: python

   await my_app.set_config(config={'redirect-map':'https://demo'})


> See more: `Application.set_config (method) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.application.html#juju.application.Application.set_config>`_,  `Application.get_config (method) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.application.html#juju.application.Application.get_config)>`_


.. _scale-an-application:
Scale an application
--------------------

> See also: :ref:`juju:scaling`

Scale an application vertically
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To scale an application vertically, set constraints for the resources that the application's units will be deployed on.

> See more: :ref:`manage-constraints-for-an-application`

Scale an application horizontally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To scale an application horizontally, control the number of units.

> See more: :ref:`control-the-number-of-units`


Make an application highly available
------------------------------------
> See also: :ref:`juju:high-availability`

1. Find out if the charm delivering the application supports high availability natively or not. If the latter, find out what you need to do. This could mean integrating with a load balancing reverse proxy, configuring storage etc.

> See more: `Charmhub <https://charmhub.io/>`_

2. Scale up horizontally as usual.

> See more: {ref}`How to scale an application horizontally <5476md>`

Every time a unit is added to an application, Juju will spread out that application's units, distributing them evenly as supported by the provider (e.g., across multiple availability zones) to best ensure high availability. So long as a cloud's availability zones don't all fail at once, and the charm and the charm's application are well written (changing leaders, coordinating across units, etc.), you can rest assured that cloud downtime will not affect your application.

> See more: `Charmhub | wordpress <https://charmhub.io/wordpress>`_, `Charmhub | mediawiki <https://charmhub.io/mediawiki>`_, `Charmhub | haproxy <https://charmhub.io/haproxy>`_

Integrate an application with another application
-------------------------------------------------

> See more: :ref:`manage-relations`


Manage an application’s public availability over the network
------------------------------------------------------------

To expose some or all endpoints of an application over a network, you may use the `Application.expose()` method, as follows:

.. code:: python

   await my_app.expose(exposed_endpoints=None) # everything's reachable from 0.0.0.0/0.


To expose to specific CIDRs or spaces, you may use an `ExposedEndpoint` object to describe that, as follows:

.. code:: python

   # For spaces
   await my_app.expose(exposed_endpoints={"": ExposedEndpoint(to_spaces=["alpha"]) })

   # For cidrs
   await my_app.expose(exposed_endpoints={"": ExposedEndpoint(to_cidrs=["10.0.0.0/24"])})

   # You may use both at the same time too
   await my_app.expose(exposed_endpoints={
               "ubuntu": ExposedEndpoint(to_spaces=["alpha"], to_cidrs=["10.0.0.0/24"])
           })



To unexpose an application, use the `Application.unexpose()` method:

.. code:: python

   await my_app.unexpose() # unexposes the entire application

   await my_app.unexpose(exposed_endpoints=["ubuntu"]) # unexposes the endpoint named "ubuntu"


> See more: `ExposedEndpoint (methods) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.application.html#juju.application.ExposedEndpoint>`_, `Application.expose() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.application.html#juju.application.Application.expose>`_,  `Application.unexpose() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.application.html#juju.application.Application.unexpose>`_


.. _manage-constraints-for-an-application:
Manage constraints for an application
-------------------------------------

> See also: :ref:`juju:constraint`

**Set values.** To set constraints for application in python-libjuju:

* To set at deployment, simply provide a `constraints` map during the `Model.deploy()` call:

.. code:: python

   await my_model.deploy(..., constraints={'arch': 'amd64', 'mem': 256}, ...)


* To set constraints post deployment, you may use the `Application.set_contraints()` method, similar to passing constraints in the deploy call above:

.. code:: python

   await my_app.set_constraints(constraints={'arch': 'amd64', 'mem': 256})


**Get values.** To see what constraints are set on an application, use the `Application.get_constraints()` method:

.. code:: python

   await my_app.get_constraints()


> See more: `Application.set_contraints() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.application.html#juju.application.Application.set_constraints>`_, `Application.get_constraints (method) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.application.html#juju.application.Application.get_constraints>`_


Change space bindings for an application
----------------------------------------

To set bindings for an application on python-libjuju, simply pass the `bind` parameter at the `Model.deploy()` call:

.. code:: python

   await my_model.deploy(..., bind="db=db db-client=db public admin-api=public", ...)

Python-libjuju currently doesn't support resetting space bindings post deployment, please use the `juju-cli` for that.

> See more: [`Model.deploy()` (method) <5476md>`

Upgrade an application
----------------------

To upgrade an application, update its charm.

> See more: :ref:`update-a-charm`

.. _remove-an-application:

Remove an application
---------------------

> See also: :ref:`juju:removing-things`

To remove an application from a model in python-libjuju, you have two choices:

(1) If you have a reference to a connected model object (connected to the model you're working on), then you may use the `Model.remove_application()` method:

.. code:: python

   await my_model.remove_application(my_app.name)


(2) If you have a reference to the application you want to remove, then you may use the `Application.destroy()` directly on the application object you want to remove:

.. code:: python

   await my_app.destroy()

> See more: `Model.remove_application (method) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.remove_application>`_, `Application.destroy (method) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.application.html#juju.application.Application.destroy>`_
