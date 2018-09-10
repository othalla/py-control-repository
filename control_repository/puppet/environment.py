from github.Repository import Repository
from github import GithubException

from control_repository.exceptions import PuppetfileNotFoundException
from control_repository.puppet.puppetfile import Puppetfile

class Environment:
    def __init__(self, name: str, github_repository: Repository) -> None:
        self._name = name
        self._github_repository = github_repository

    def get_puppetfile(self) -> Puppetfile:
        try:
            self._github_repository.get_file_contents('/Puppetfile',
                                                      ref=self._name)
            return Puppetfile()
        except GithubException:
            raise PuppetfileNotFoundException
