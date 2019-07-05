import sys
from os import environ

from cliff.app import App
from cliff.command import Command
from cliff.commandmanager import CommandManager
from cliff.lister import Lister

from control_repository.control_repository import ControlRepository


class MyApp(App):
    def __init__(self):
        super().__init__(
            description='Command line for puppet control repository',
            version='0.1',
            command_manager=CommandManager('myapp'),
            deferred_help=True,
        )

    def initialize_app(self, argv):
        commands = [EnvironmentList,
                    EnvironmentModuleList,
                    EnvironmentModuleForgeList,
                    EnvironmentModuleForgeAdd,
                    EnvironmentModuleForgeRemove,
                    EnvironmentModuleForgeUpdate,
                    EnvironmentModuleGitList,
                    EnvironmentModuleGitAdd]
        for command in commands:
            self.command_manager.add_command(command.name, command)


class EnvironmentList(Lister):
    """List all Puppet environments"""

    name = 'environment list'

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('--url',
                            default=None,
                            help='github url of the control repository')
        return parser

    def take_action(self, parsed_args):
        organisation, repository, token = get_config_from_environment()
        control_repository = ControlRepository(organisation,
                                               repository,
                                               token,
                                               parsed_args.url)
        environment_list = control_repository.get_environment_names()
        return (('Name',), ((env,) for env in environment_list))


class EnvironmentModuleForgeList(Lister):
    """List all forge module for a specific environment"""

    name = 'environment module forge list'

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('name',
                            help='Name of the environment',
                            nargs=1)
        parser.add_argument('--url',
                            default=None,
                            help='github url of the control repository')
        return parser

    def take_action(self, parsed_args):
        organisation, repository, token = get_config_from_environment()
        control_repository = ControlRepository(organisation,
                                               repository,
                                               token,
                                               parsed_args.url)
        puppet_environment = control_repository.get_environment(
            parsed_args.name[0])
        puppetfile = puppet_environment.get_puppetfile()
        forge_modules = puppetfile.forge_modules
        return (('Name', 'version'),
                ((module.name,
                  module.version if module.version else '')
                 for module in forge_modules))


class EnvironmentModuleGitList(Lister):
    """List all git module for a specific environment"""

    name = 'environment module git list'

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('name',
                            help='Name of the environment',
                            nargs=1)
        parser.add_argument('--url',
                            default=None,
                            help='github url of the control repository')
        return parser

    def take_action(self, parsed_args):
        organisation, repository, token = get_config_from_environment()
        control_repository = ControlRepository(organisation,
                                               repository,
                                               token,
                                               parsed_args.url)
        puppet_environment = control_repository.get_environment(
            parsed_args.name[0])
        puppetfile = puppet_environment.get_puppetfile()
        git_modules = puppetfile.git_modules
        return (('Name', 'url', 'reference_type', 'referece'),
                ((module.name,
                  module.git_url,
                  module.reference_type if module.reference_type else '',
                  module.reference if module.reference else '')
                 for module in git_modules))


class EnvironmentModuleForgeAdd(Command):
    """Add a forge module from a specific environment"""

    name = 'environment module forge add'

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('environment',
                            help='Name of the environment',
                            nargs=1)
        parser.add_argument('module',
                            help='Name of the module',
                            nargs=1)
        parser.add_argument('--module_version',
                            help='version of the forge module',
                            default=None)
        parser.add_argument('--url',
                            default=None,
                            help='github url of the control repository')
        return parser

    def take_action(self, parsed_args):
        organisation, repository, token = get_config_from_environment()
        control_repository = ControlRepository(organisation,
                                               repository,
                                               token,
                                               parsed_args.url)
        puppet_environment = control_repository.get_environment(
            parsed_args.environment[0])
        puppetfile = puppet_environment.get_puppetfile()
        puppetfile.add_forge_module(parsed_args.module[0],
                                    parsed_args.module_version)


class EnvironmentModuleGitAdd(Command):
    """Add a git module to a specific environment"""

    name = 'environment module git add'

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('environment',
                            help='Name of the environment',
                            nargs=1)
        parser.add_argument('module',
                            help='Name of the module',
                            nargs=1)
        parser.add_argument('url',
                            help='GitHub URL of the git module to add',
                            nargs=1)
        parser.add_argument('--reference_type',
                            default=None,
                            help=('Git reference type to check out: '
                                  'Tag, commit or branch.'))
        parser.add_argument('--reference',
                            default=None,
                            help='Git reference to check out.')
        parser.add_argument('--url',
                            default=None,
                            help='github url of the control repository')
        return parser

    def take_action(self, parsed_args):
        if not parsed_args.reference or not parsed_args.reference_type:
            exit('You must provide either a git reference type and a'
                 'git reference.')
        organisation, repository, token = get_config_from_environment()
        control_repository = ControlRepository(organisation,
                                               repository,
                                               token,
                                               parsed_args.url)
        puppet_environment = control_repository.get_environment(
            parsed_args.environment[0])
        puppetfile = puppet_environment.get_puppetfile()
        puppetfile.add_git_module(parsed_args.module[0],
                                  parsed_args.url[0],
                                  reference_type=parsed_args.reference_type,
                                  reference=parsed_args.reference)


class EnvironmentModuleForgeUpdate(Command):
    """Update a forge module from a specific environment"""

    name = 'environment module forge update'

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('environment',
                            help='Name of the environment',
                            nargs=1)
        parser.add_argument('module',
                            help='Name of the module',
                            nargs=1)
        parser.add_argument('module_version',
                            help='version of the forge module',
                            nargs=1)
        parser.add_argument('--url',
                            default=None,
                            help='github url of the control repository')
        return parser

    def take_action(self, parsed_args):
        organisation, repository, token = get_config_from_environment()
        control_repository = ControlRepository(organisation,
                                               repository,
                                               token,
                                               parsed_args.url)
        puppet_environment = control_repository.get_environment(
            parsed_args.environment[0])
        puppetfile = puppet_environment.get_puppetfile()
        puppetfile.update_forge_module(parsed_args.module[0],
                                       parsed_args.module_version[0])


class EnvironmentModuleForgeRemove(Command):
    """Remove a forge module from a specific environment"""

    name = 'environment module forge remove'

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('environment',
                            help='Name of the environment',
                            nargs=1)
        parser.add_argument('module',
                            help='Name of the module',
                            nargs=1)
        parser.add_argument('--url',
                            default=None,
                            help='github url of the control repository')
        return parser

    def take_action(self, parsed_args):
        organisation, repository, token = get_config_from_environment()
        control_repository = ControlRepository(organisation,
                                               repository,
                                               token,
                                               parsed_args.url)
        puppet_environment = control_repository.get_environment(
            parsed_args.environment[0])
        puppetfile = puppet_environment.get_puppetfile()
        puppetfile.remove_forge_module(parsed_args.module[0])


class EnvironmentModuleList(Lister):
    """List all modules for a specific environment"""

    name = 'environment module list'

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument('name',
                            help='Name of the environment',
                            nargs=1)
        parser.add_argument('--url',
                            default=None,
                            help='github url of the control repository')
        return parser

    def take_action(self, parsed_args):
        organisation, repository, token = get_config_from_environment()
        control_repository = ControlRepository(organisation,
                                               repository,
                                               token,
                                               parsed_args.url)
        puppet_environment = control_repository.get_environment(
            parsed_args.name[0])
        puppetfile = puppet_environment.get_puppetfile()
        module_list = puppetfile.list_modules()
        return (('Name',), ((module,) for module in module_list))


def get_config_from_environment():
    organisation = environ.get('GITHUB_ORGANISATION')
    if not organisation:
        exit('No github organisation provided. '
             'You can set it with GITHUB_ORGANISATION environment var.')
    repository = environ.get('GITHUB_REPOSITORY')
    if not repository:
        exit('No github repository provided. '
             'You can set it with GITHUB_REPOSITORY environment var.')
    token = environ.get('GITHUB_ACCESS_TOKEN')
    if not token:
        exit('No github access token provided. '
             'You can set it with GITHUB_ACCESS_TOKEN environment var.')
    return organisation, repository, token


def main():
    argv = sys.argv[1:]
    myapp = MyApp()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main())
