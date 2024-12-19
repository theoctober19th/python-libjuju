.. _manage-relations:

How to manage relations
=======================

> See also: :ref:`juju:relation`

Add a relation
--------------

The procedure differs slightly depending on whether the applications that you want to integrate are on the same model or rather on different models.

Add a same-model relation
~~~~~~~~~~~~~~~~~~~~~~~~~
> See also: :ref:`juju:same-model-relation`

To add a same-model relation between two applications, on a connected Model, use the `integrate()` method.

.. code:: python

   await my_model.integrate('mysql', 'mediawiki')

   # Integrate with particular endpoints
   await my_model.integrate('mysql', 'mediawiki:db')


> See more: `integrate() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.integrate>`_

Add a cross-model relation
~~~~~~~~~~~~~~~~~~~~~~~~~~
> See also: :ref:`juju:cross-model-relation`


In a cross-model relation there is also an 'offering' model and a 'consuming' model. The admin of the 'offering' model 'offers' an application for consumption outside of the model and grants an external user access to it. The user on the 'consuming' model can then find an offer to use, consume the offer, and integrate an application on their model with the 'offer' via the same `integrate` command as in the same-model case (just that the offer must be specified in terms of its offer URL or its consume alias). This creates a local proxy for the offer in the consuming model, and the application is subsequently treated as any other application in the model.

> See more: :ref:`integrate-with-an-offer`

View all the current relations
------------------------------

To view the current relations in a model, directly access the Model's `relations` property.

.. code:: python

   my_model.relations

> See more: `Model.relations (property) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.relations>`_


Remove a relation
-----------------

To remove a relation, use the `remove_relation()` method on an Application object.

.. code:: python

   await my_app.remove_relation('mediawiki', 'mysql:db')

> See more: `remove_relation() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.application.html#juju.application.Application.remove_relation>`_
