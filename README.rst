================================================================
Py Control Repository - Python SDK for Puppet Control Repository
================================================================

.. image:: https://travis-ci.org/othalla/py-control-repository.svg?branch=master
    :target: https://travis-ci.org/othalla/py-control-repository
.. image:: https://badge.fury.io/py/py-control-repository.svg
    :target: https://badge.fury.io/py/py-control-repository
.. image:: https://codecov.io/gh/othalla/py-control-repository/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/othalla/py-control-repository

Py Control Repository is SDK for Pyththon which allows developpers
to manage a Puppet Control Repository based on GitHub.


Install
-------

.. code-block:: sh

    $ pip install py-control-repository

Usage
-----

Get Puppetfile
~~~~~~~~~~~~~~

.. code-block:: python

   control_repository = ControlRepository('myorga', 'my_control_repository', 'token')

   puppet_environment = control_repository.get_environent('production')

   puppetfile = puppet_environment.get_puppetfile()

Add a custom forge URL
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   puppetfile.set_forge_url('https://urlcustomforge.com/forge')

Add a forge module
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   puppetfile.add_forge_module('puppetlabs/apache', version='0.10.1')

Update a forge module
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   puppetfile.update_forge_module('puppetlabs/apache', '0.11.0')
