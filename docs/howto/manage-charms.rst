.. _manage-charms:

How to manage charms or bundles
===============================
> See also: :ref:`juju:charm`

This document shows various ways in which you may interact with a charm or a bundle.


Query Charmhub for available charms / bundles
---------------------------------------------

To query Charmhub for the charms / bundles on python-libjuju, you can use the `find` method on the `CharmHub` object that's built-in on each `Model` object:

.. code:: python

   await model.charmhub.find('wordpress')



View details about a Charmhub charm / bundle
--------------------------------------------

To view details about a particular Charmhub charm / bundle on python-libjuju, you can use the `info` method on the `CharmHub` object that's built-in on each `Model` object:

.. code:: python

   await model.charmhub.info('wordpress')



Find out the resources available for a charm
--------------------------------------------

> See more: :ref:`manage-charm-resources`

.. _deploy-a-charm:
Deploy a charm / bundle
-----------------------

To deploy a Charmhub charm / bundle using python-libjuju, you can use the `deploy` method on the `Model` object:


.. code:: python

   m = model.Model()
   await m.connect()

   # deploy a charm
   await m.deploy('mysql')

   # deploy a bundle
   await m.deploy('kubeflow')

   # deploy a local charm
   await m.deploy('./mini_ubuntu-20.04-amd64.charm')

   # deploy a local charm with a resource
   await m.deploy('./demo-api-charm_ubuntu-22.04-amd64.charm', resources={'demo-server-image=ghcr.io/beliaev-maksim/api_demo_server':'0.0.9'})

   # deploy a local bundle
   await m.deploy('./mediawiki-model-bundle.yaml')

   # deploy a bundle with an overlay
   await m.deploy('mediawiki', overlays=['./custom-mediawiki.yaml'])

   # generic openstack example
   await m.deploy('./bundle-focal-yoga.yaml', overlays=['./overlay-focal-yoga-mymaas.yaml', './overlay-focal-yoga-mymaas-shared-filesystem.yaml'])


> See more:  `Model.deploy() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.deploy>`_


.. _update-a-charm:
Update a charm
--------------

To update a charm on python-libjuju, you can use the `upgrade_charm` (aliased as `refresh`) method on the `Application` object:

.. code:: python

   # upgrade to latest revision on the channel
   await my_app.upgrade_charm()

   # upgrade to the latest revision on a given channel
   await my_app.upgrade_charm(channel='latest/edge')

   # upgrade to a particular revision
   await my_app.upgrade_charm(revision=3)

   # upgrade with a local charm
   await my_app.upgrade_charm(path='./path/to/juju-test')

   # replace a charm completely with another charm
   await my_app.upgrade_charm(switch='./path/to/juju-test')

   # Note that the path and switch parameters are mutually exclusive.

> See more:  `Application.upgrade_charm() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.application.html#juju.application.Application.upgrade_charm>`_


Remove a charm / bundle
-----------------------

As a charm / bundle is just the *means* by which (an) application(s) are deployed, there is no way to remove the *charm* / *bundle*. What you *can* do, however, is remove the *application* / *model*.

> See more: :ref:`remove-an-application`
