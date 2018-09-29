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

Get Puppet Environment
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   control_repository = ControlRepository('myorga', 'my_control_repository', 'token')

   puppet_environment = control_repository.get_environent('production')

Get Puppetfile
~~~~~~~~~~~~~~

.. code-block:: python

   puppetfile = puppet_environment.get_puppetfile()

List Puppet modules in Puppetfile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   module_list = puppetfile.list_modules()

Add a custom forge URL
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   puppetfile.set_forge_url('https://urlcustomforge.com/forge')

Remove a custom forge URL
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   puppetfile.remove_forge_url()

Add a forge module
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   puppetfile.add_forge_module('puppetlabs/apache', version='0.10.1')

Update a forge module
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   puppetfile.update_forge_module('puppetlabs/apache', '0.11.0')

Add a git module
~~~~~~~~~~~~~~~~

With no version spicified, it will install the current master branch.

.. code-block:: python

   puppetfile.add_git_module('custom_module', 'https://url.my.git/orga/custom_module')

You can specify a specific git reference. Supported are :

- branch
- ref
- tag
- commit

.. code-block:: python

   puppetfile.add_git_module('custom_module',
                             'https://url.my.git/orga/custom_module',
                             reference_type='commit',
                             reference='ae1fe')
