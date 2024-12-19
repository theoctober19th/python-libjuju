.. _manage-credentials:

How to manage credentials
=========================

> See also: :ref:`juju:credential`


Update a credential
-------------------

To update a credential, on a connected `Controller` object, use the `Controller.add_credential()` method. `add_credential` is an upsert method (where it inserts if the given credential is new, and updates if the given credential name already exists).

.. code:: python

   from juju.client import client as jujuclient

   my_controller.add_credential("my-credential",
       jujuclient.CloudCredential(auth_type="jsonfile", attrs={'file':'path_to_cred_file'}))

> See more: `add_credential (method) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.controller.html#juju.controller.Controller.add_credential>`_
