# py-control-repository

[![Build Status](https://travis-ci.org/othalla/py-control-repository.svg?branch=master)](https://travis-ci.org/othalla/py-control-repository)
[![PyPI version](https://badge.fury.io/py/py-control-repository.svg)](https://badge.fury.io/py/py-control-repository)

## Description

This module aims to manage a Puppet control repository hosted on Github.
It allow to manage Puppetfile's module (add, update, update) in a specific Puppet environment.

## Usage


### Add a forge module

```
control_repository = ControlRepository('myorga', 'my_control_repository', 'token')

puppet_environment = control_repository.get_environent('production')

puppetfile = puppet_environment.get_puppetfile()

puppetfile.add_forge_module('puppetlabs/apache', version='0.10.1')
```

