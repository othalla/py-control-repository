import sys
from os import environ

from cliff.app import App
from cliff.commandmanager import CommandManager
from cliff.lister import Lister

ENVS = ['dev', 'production']


class MyApp(App):
    def __init__(self):
        super().__init__(
            description='Command line for puppet control repository',
            version='0.1',
            command_manager=CommandManager('myapp'),
            deferred_help=True,
        )

    def initialize_app(self, argv):
        commands = [EnvironmentList, ]
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
        token = environ.get('ACCESS_TOKEN')
        if not token:
            exit('No github access token provided. '
                 'You can set it with ACCESS_TOKEN environment var.')
        print(token)
        print(parsed_args.url)
        return (('Name',), ((env,) for env in ENVS))


def main():
    argv = sys.argv[1:]
    myapp = MyApp()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main())
