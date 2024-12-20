.. _manage-python-libjuju:

How to manage python-libjuju
============================

> See also: :ref:`juju:client`


Install `python-libjuju`
------------------------

In PyPI, which is the Python repository that `pip` is drawing modules from, `python-libjuju` is simply referred to as `juju`. You can install it directly via `pip`:

.. code:: bash

   pip3 install juju


Use `python-libjuju`
--------------------

1. After installing `python-libjuju`, import it into your Python script as follows:

.. code::

  import juju

You can also import specific modules to use, depending on your use case:

.. code::

  from juju import model

or

.. code::

  from juju import controller


Examples of different use cases of this client can be found in the docs, as well as in the `examples
directory in the repository <https://github.com/juju/python-libjuju/tree/master/examples>`_ which can be run using ``tox``.  For
example, to run ``examples/connect_current_model.py``, use:

.. code:: bash

  tox -e example -- examples/connect_current_model.py


Or you can directly run it via python as well:

.. code::

   $ python3 examples/connect_current_model.py


To experiment with the library in a REPL, launch Python repl with asyncio module loaded, as follows:

.. code::

  $ python3 -m asyncio

and then, for example to connect to the current model and fetch status:

.. code::

  >>> from juju.model import Model
  >>> model = Model()
  >>> await model.connect_current()
  >>> status = await model.get_status()

Whichever your chosen method, use the `python-libjuju` how-to guides and the reference to build up your deployment.
