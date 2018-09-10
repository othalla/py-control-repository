from typing import Optional

from github import Github, GithubException
from github.Repository import Repository

from control_repository.exceptions import (ControlRepositoryException,
                                           EnvironmentNotFoundException)
from control_repository.puppet.environment import Environment


class ControlRepository:
    def __init__(self, github_organization: str,
                 github_repository_name: str,
                 github_token: str,
                 github_baseurl: Optional[str] = None) -> None:
        self._github_organization: str = github_organization
        self._github_repository_name: str = github_repository_name
        self._github_token: str = github_token
        self._github_baseurl: Optional[str] = github_baseurl
        self._github_repository: Repository = self._get_github_repository()

    def get_environment(self, environment: str) -> Environment:
        try:
            self._github_repository.get_branch(environment)
        except GithubException:
            raise EnvironmentNotFoundException
        return Environment(environment, self._github_repository)

    def _get_github_repository(self) -> Repository:
        try:
            github = Github(self._github_token)
            organization = github.get_organization(self._github_organization)
            return organization.get_repo(self._github_repository_name)
        except GithubException:
            raise ControlRepositoryException
