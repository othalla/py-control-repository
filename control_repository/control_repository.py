from github import Github, GithubException

from control_repository.exceptions import (ControlRepositoryException,
                                           EnvironmentNotFoundException)
from control_repository.puppet import Environment


class ControlRepository:
    def __init__(self, github_organization: str,
                 github_repository: str,
                 github_token: str,
                 github_baseurl=None) -> None:
        self._github_organization = github_organization
        self._github_repository = github_repository
        self._github_token = github_token
        self._github_baseurl = github_baseurl
        self._github_repository = self._get_github_repository()

    def get_environment(self, environment):
        try:
            self._github_repository.get_branch(environment)
        except GithubException:
            raise EnvironmentNotFoundException
        return Environment()

    def _get_github_repository(self):
        try:
            github = Github(self._github_token)
            organization = github.get_organization(self._github_organization)
            return organization.get_repo(self._github_repository)
        except GithubException:
            raise ControlRepositoryException
