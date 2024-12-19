.. _manage-ssh-keys:

How to manage SSH keys
======================

> See also: :ref:`juju:ssh-key`


Add an SSH key
--------------

To add a public `ssh` key to a model, on a connected Model object, use the `add_ssh_key()` method, passing a name for the key and the actual key payload. For example:

.. code:: python

   SSH_KEY = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC1I8QDP79MaHEIAlfh933zqcE8LyUt9doytF3YySBUDWippk8MAaKAJJtNb+Qsi+Kx/RsSY02VxMy9xRTp9d/Vr+U5BctKqhqf3ZkJdTIcy+z4hYpFS8A4bECJFHOnKIekIHD9glHkqzS5Vm6E4g/KMNkKylHKlDXOafhNZAiJ1ynxaZIuedrceFJNC47HnocQEtusPKpR09HGXXYhKMEubgF5tsTO4ks6pplMPvbdjxYcVOg4Wv0N/LJ4ffAucG9edMcKOTnKqZycqqZPE6KsTpSZMJi2Kl3mBrJE7JbR1YMlNwG6NlUIdIqVoTLZgLsTEkHqWi6OExykbVTqFuoWJJY3BmRAcP9H3FdLYbqcajfWshwvPM2AmYb8V3zBvzEKL1rpvG26fd3kGhk3Vu07qAUhHLMi3P0McEky4cLiEWgI7UyHFLI2yMRZgz23UUtxhRSkvCJagRlVG/s4yoylzBQJir8G3qmb36WjBXxpqAGHfLxw05EQI1JGV3ReYOs= user@somewhere"
   await my_model.add_ssh_key('admin', SSH_KEY)


> See more: `add_ssh_key() https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.add_ssh_key>`_, `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_


View the available SSH keys
---------------------------

To list the currently known SSH keys for the current model, on a connected Model object, use the `get_ssh_keys()` method. For example:

.. code:: python

   await my_model.get_ssh_keys()


> See more: `get_ssh_keys() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.get_ssh_keys>`_, `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_


Remove an SSH key
-----------------

To remove an SSH key, on a connected Model object, use the `remove_ssh_key()` method, passing the user name and the key as parameters. For example:

.. code:: python

   SSH_KEY = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC1I8QDP79MaHEIAlfh933zqcE8LyUt9doytF3YySBUDWippk8MAaKAJJtNb+Qsi+Kx/RsSY02VxMy9xRTp9d/Vr+U5BctKqhqf3ZkJdTIcy+z4hYpFS8A4bECJFHOnKIekIHD9glHkqzS5Vm6E4g/KMNkKylHKlDXOafhNZAiJ1ynxaZIuedrceFJNC47HnocQEtusPKpR09HGXXYhKMEubgF5tsTO4ks6pplMPvbdjxYcVOg4Wv0N/LJ4ffAucG9edMcKOTnKqZycqqZPE6KsTpSZMJi2Kl3mBrJE7JbR1YMlNwG6NlUIdIqVoTLZgLsTEkHqWi6OExykbVTqFuoWJJY3BmRAcP9H3FdLYbqcajfWshwvPM2AmYb8V3zBvzEKL1rpvG26fd3kGhk3Vu07qAUhHLMi3P0McEky4cLiEWgI7UyHFLI2yMRZgz23UUtxhRSkvCJagRlVG/s4yoylzBQJir8G3qmb36WjBXxpqAGHfLxw05EQI1JGV3ReYOs= user@somewhere"
   await my_model.remove_ssh_key('admin', SSH_KEY)

> See more: `remove_ssh_key() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.remove_ssh_key>`_, `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_
