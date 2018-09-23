from github.Repository import Repository

from control_repository.puppet.puppetfile import Puppetfile


class Environment:
    def __init__(self, name: str, github_repository: Repository) -> None:
        self._name: str = name
        self._github_repository: Repository = github_repository

    def get_puppetfile(self) -> Puppetfile:
        return Puppetfile.from_github_repository(self._github_repository,
                                                 self._name)
