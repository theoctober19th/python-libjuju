.. _manage-offers:

How to manage offers
====================

> See also: :ref:`juju:offer`

This document shows how to manage offers.


Create an offer
---------------
> Who: User with :ref:`juju:user-access-offer-admin`

To create an offer, use the `create_offer()` method on a connected Model object.

.. code:: python

   # Assume a deployed mysql application
   await my_model.deploy('mysql')
   # Expose the database endpoint of the mysql application
   await my_model.create_offer('mysql:database', offer_name='hosted-mysql')

> See more: `create_offer() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.create_offer>`_


Control access to an offer
--------------------------
> Who: User with :ref:`juju:user-access-offer-admin`

The access levels for offers can be applied in the same way the model or controller access for a given user. Use the `grant()` and `revoke()` methods on a User object to grant or revoke access to an offer.

.. code:: python

   # Grant Bob consume access to an offer
   await user_bob.grant('consume', offer_name='admin/default.hosted-mysql')

   # Revoke Bob's consume access (he will be left with read access)
   await user_bob.revoke('consume', offer_name='admin/default.hosted-mysql')

> See more: `User (object)`


.. _integrate-with-an-offer:
Integrate with an offer
-----------------------
> Who: User with :ref:`juju:user-access-offer-consume`

To integrate with an offer, on a connected model, use the `Model.integrate()` method with a consumed offer url. For example:

.. code:: python

   # Integrate via offer url
   await my_model.integrate('mediawiki:db', 'admin/default.hosted-mysql')

   # Integrate via an offer alias created when consumed
   await my_model.consume('admin/prod.hosted_mysql', application_alias="mysql-alias")
   await my_model.integrate('mediawiki:db', 'mysql-alias')

   # Remove a consumed offer:
   await my_model.remove_saas('mysql-alias')

> See more: `Model.integrate() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.integrate>`_, `Model.consume() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.consume>`_, `Model.remove_saas() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.remove_saas>`_


Inspect integrations with an offer
----------------------------------
> Who: User with :ref:`juju:user-access-offer-admin`

To see all connections to one or more offers, use the `list_offers()` method on a connected Model object.

.. code:: python

   await my_model.list_offers()

> See more: `list_offers() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.list_offers>`_


Remove an offer
---------------
> Who: User with :ref:`juju:user-access-offer-admin`

To remove an offer, use the `remove_offer()` method on a connected Model. If the offer is used in an integration, then the `force=True` parameter is required to remove the offer, in which case the integration is also removed.

.. code:: python

   await my_model.remove_offer('admin/mymodel.ubuntu', force=True)

> See more: `remove_offer() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.remove_offer>`_
