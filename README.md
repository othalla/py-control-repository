# py-puppetfile

## Usage


## Refactor model 

```
control_repository = ControlRepository('orga', 'repo', 'token')

puppet_environment = control_repository.get_environent('production')
```

```
puppetfile = puppet_environment.get_puppetfile()

puppetfile.add_forge_module(module)
```

