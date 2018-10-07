from typing import Optional, List

from github import Github, GithubException
from github.Repository import Repository

from control_repository.exceptions import (ControlRepositoryException,
                                           EnvironmentNotFoundException)
from control_repository.environment import Environment


class ControlRepository:
    """
    This class represents a Puppet control repository hosted on github.

    :type github_organization: string
    :param github_organization: The name of the Github organization
    :type github_repository_name: string
    :param github_repository_name: The name of the Github repository
    :type github_token: string
    :param github_token: The Github token for authentication
    :type github_baseurl: string
    :param github_baseurl: The url of the Github server
    """

    def __init__(self,
                 github_organization: str,
                 github_repository_name: str,
                 github_token: str,
                 github_baseurl: Optional[str] = None) -> None:
        self._github_organization: str = github_organization
        self._github_repository_name: str = github_repository_name
        self._github_token: str = github_token
        self._github_baseurl: Optional[str] = github_baseurl
        self._github_repository: Repository = self._get_github_repository()

    def get_environment(self, environment: str) -> Environment:
        """
        Returns a Puppet environment.

        :type environment: string
        :param environment: The name of the Puppet environment
        :rtype: :class:`control_repository.environment.Environment`
        :return: Puppet Environment object
        """
        try:
            self._github_repository.get_branch(environment)
        except GithubException:
            raise EnvironmentNotFoundException
        return Environment(environment, self._github_repository)

    def get_environments(self) -> List[Environment]:
        """
        Returns the list of all Puppet environments in the control repository.

        :rtype: list of :class:`control_repository.environment.Environment`
        :return: the list of Puppet Environment object
        """
        branches = self._github_repository.get_branches()
        environments = []
        for branch in branches:
            environments.append(Environment(branch.name,
                                            self._github_repository))
        return environments

    def get_environment_names(self) -> List[str]:
        """
        Returns the list of all environments names.

        :rtype: list of string
        :return: the list of environments names.
        """
        branches = self._github_repository.get_branches()
        return [branch.name for branch in branches]

    def _get_github_repository(self) -> Repository:
        try:
            github = Github(self._github_token)
            organization = github.get_organization(self._github_organization)
            return organization.get_repo(self._github_repository_name)
        except GithubException:
            raise ControlRepositoryException
