================================================================
Py Control Repository - Python SDK for Puppet Control Repository
================================================================

.. image:: https://travis-ci.org/othalla/py-control-repository.svg?branch=master
    :target: https://travis-ci.org/othalla/py-control-repository
.. image:: https://badge.fury.io/py/py-control-repository.svg
    :target: https://badge.fury.io/py/py-control-repository
.. image:: https://codecov.io/gh/othalla/py-control-repository/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/othalla/py-control-repository
.. image:: https://api.codacy.com/project/badge/Grade/f631643ebb164aa697cb40c63f6d8375
  :target: https://www.codacy.com/app/othalla/py-control-repository?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=othalla/py-control-repository&amp;utm_campaign=Badge_Grade

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

   puppet_environment = control_repository.get_environment('production')

Get all Puppet Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns the list of all Puppet Environment.

.. code-block:: python

   control_repository = ControlRepository('myorga', 'my_control_repository', 'token')

   puppet_environments = control_repository.get_environments()

Get all Puppet Environment names
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns the list of all Puppet Environment names.

.. code-block:: python

   control_repository = ControlRepository('myorga', 'my_control_repository', 'token')

   puppet_environment_names = control_repository.get_environment_names()

Get Puppetfile
~~~~~~~~~~~~~~

.. code-block:: python

   puppetfile = puppet_environment.get_puppetfile()

List Puppet modules in Puppetfile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   module_list = puppetfile.list_modules()

Add a forge module
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   puppetfile.add_forge_module('puppetlabs/apache', version='0.10.1')

Update a forge module
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   puppetfile.update_forge_module('puppetlabs/apache', '0.11.0')

Remove a forge module
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   puppetfile.remove_forge_module('puppetlabs/apache')

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

Update a git module
~~~~~~~~~~~~~~~~~~~

Bump module version

.. code-block:: python

   puppetfile.update_git_module('mymodule', '12.0.2')

You can also change a module reference type and its value.

For example you have a module deployed by its master branch and want to track it by a specific tag.

.. code-block:: python

   puppetfile.update_git_module('mymodule', '1.0.0', reference_type='tag')
