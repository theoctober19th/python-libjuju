.. _manage-actions:

How to manage actions
=====================


> See also: :ref:`juju:action`



List all actions
----------------


To list the actions defined for a deployed application, use the `get_actions()` method on the `Application` object to get all the actions defined for this application.

.. code:: python

   await my_app.get_actions()


> See more: `Application (object) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/application.html>`_, `get_actions (method) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.application.html#juju.application.Application.get_actions>`_


Run an action

To run an action on a unit, use the `run_action()` method on a Unit object of a deployed application.

Note that "running" an action on a unit, enqueues an action to be performed. The result will be an Action object to interact with. You will need to call `action.wait()` on that object to wait for the action to complete and retrieve the results.

.. code:: python

   # Assume we deployed a git application
   my_app = await model.deploy('git', application_name='git', channel='stable')
   my_unit = my_app.units[0]

   action = await my_unit.run_action('add-repo', repo='myrepo')
   await action.wait() # will return the result for the action

> See more: `Unit (object) <https://pythonlibjuju.readthedocs.io/en/latest/narrative/unit.html>`_, `Action (object) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.action.html#juju.action.Action>`_, `Unit.run_action (method) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.unit.html#juju.unit.Unit.run_action>`_, `Action.wait() (method) <https://pythonlibjuju.readthedocs.io/en/latest/api/juju.action.html#juju.action.Action.wait>`_
