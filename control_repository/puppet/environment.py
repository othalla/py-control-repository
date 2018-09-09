from github.Repository import Repository

from control_repository.puppet.puppetfile import Puppetfile

class Environment:
    def __init__(self, name: str, github_repository: Repository) -> None:
        self._name = name
        self._github_repository = github_repository

    def get_puppetfile(self) -> Puppetfile:
        return Puppetfile()
