.. _manage-machines:

How to manage machines
======================

> See also: :ref:`juju:machine`


Add a machine
-------------


To add a machine to a model, on a connected Model object, use the `add_machine()` method. For example:

.. code:: python

   await my_model.add_machine()


> See more: `add_machine() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.add_machine>`_, `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_



List all machines
-----------------

To see a list the names of all the available machines on a model, on a connected Model object, use the `get_machines()` method. For example:

.. code:: python

   await my_model.get_machines()


To get a list of the machines as Machine objects on a model, use the `machines` property on the Model object. This allows direct interaction with any of the machines on the model. For example:

.. code:: python

   machines = my_model.machines
   my_machine = machines[0] # Machine object
   print(my_machine.status)


> See more: `get_machines() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.get_machines>`_, `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_, `Model.machines (property) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.machines>`_, `Machine (object) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.machine.html#juju.machine.Machine>`_


View details about a machine
----------------------------

To see details about a machine, on a connected Model object, get a hold of the Machine object within the model using the `machines` property. This allows direct interaction with the machine, such as accessing all the details (via the object properties) for that machine. For example:

.. code:: python

   my_machine = await my_model.machines[0]
   # Then we can access all the properties to view details
   print(my_machine.addresses)
   print(my_machine.agent_version)
   print(my_machine.hostname)
   print(my_machine.status)


> See more: `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_, `Model.machines (property) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.machines>`_, `Machine (object) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.machine.html#juju.machine.Machine>`_

Show the status of a machine
----------------------------

To see the status of a machine, on a connected Model object, get a hold of the Machine object within the model using the `machines` property. The status is then retrieved directly via the Machine object properties, in this case the `status` property. For example:

.. code:: python

   my_machine = await my_model.machines[0]
   print(my_machine.status)


> See more: `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_, `Model.machines (property) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.machines>`_, `Machine (object) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.machine.html#juju.machine.Machine>`_, `Machine.status (property) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.machine.html#juju.machine.Machine.status>`_


Manage constraints for a machine
--------------------------------
> See also: :ref:`juju:constraint`

**Set values.** To set constraint values for an individual machine when you create it manually, on a connected Model, use the `add_machine()` method, passing constraints as a parameter. For example:

.. code:: python

   machine = await model.add_machine(
               constraints={
                   'arch': 'amd64',
                   'mem': 256 * MB,
               })


**Get values.** The `python-libjuju` client does not currently support getting constraint values for for an individual machine. However, to retrieve machine constraints on a model, on a connected Model, use the `get_constraints()` method. For example:

.. code:: python

   await my_model.get_constraints()


Note that this will return `None` if no constraints have been set on the model.

> See more: `add_machine() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.add_machine>`_,  `get_constraints() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.model.html#juju.model.Model.get_constraints>`_, `Model (module) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/model.html>`_


Execute a command inside a machine
----------------------------------

To run a command in a machine, on a Machine object, use the `ssh()` method, passing a command as a parameter. For example:

.. code:: python

   output = await my_machine.ssh("echo test")
   assert 'test' in output


To run a command in all the machines corresponding to an application, on an Application object, use the `run()` method, passing the command as a parameter. For example:

.. code:: python

   output = await my_application.run("echo test")
   assert 'test' in output



> See more: `ssh() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.machine.html#juju.machine.Machine.ssh>`_, `Machine (object) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.machine.html#juju.machine.Machine>`_, `run() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.application.html#juju.application.Application.run>`_, `Application (object) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/application.html>`_


Copy files securely between machines
------------------------------------

To copy files securely between machines, on a Machine object, use the `scp_to()` and `scp_from()` methods, passing source and destination parameters for the transferred files or directories. For example:

.. code:: python

   # Transfer from local machine to Juju machine represented by my_machine object
   with open(file_name, 'r') as f:
       await my_machine.scp_to(f.name, 'testfile')

   # Transfer from my_machine to local machine
   with open(file_name, 'w') as f:
       await my_machine.scp_from('testfile', f.name)
       assert f.read() == b'contents_of_file'

   # Pass -r for recursively copy a directory via the `scp_opts` parameter.
   await my_machine.scp_to('my_directory', 'testdirectory', scp_opts=['-r'])


> See more: `scp_to() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.machine.html#juju.machine.Machine.scp_to>`_, `scp_from() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.machine.html#juju.machine.Machine.scp_from>`_, `Machine (object) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.machine.html#juju.machine.Machine>`_



Remove a machine
----------------
> See also: :ref:`juju:removing-things`

To remove a machine, on a Machine object, use the `destroy()` method. For example:

.. code:: python

   await my_machine.destroy()

> See more: `destroy() <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.machine.html#juju.machine.Machine.destroy>`_, `Machine (object) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.machine.html#juju.machine.Machine>`_
