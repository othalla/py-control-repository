================================================================
Py Control Repository - Python SDK for Puppet Control Repository
================================================================

.. image:: https://travis-ci.org/othalla/py-control-repository.svg?branch=master
    :target: https://travis-ci.org/othalla/py-control-repository

Py Control Repository is SDK for Pyththon which allows developpers
to manage a Puppet Control Repository based on GitHub.


Install
-------

.. code-block:: sh

    $ pip install py-control-repository

Usage
-----

Add a forge module
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   control_repository = ControlRepository('myorga', 'my_control_repository', 'token')

   puppet_environment = control_repository.get_environent('production')

   puppetfile = puppet_environment.get_puppetfile()

   puppetfile.add_forge_module('puppetlabs/apache', version='0.10.1')
