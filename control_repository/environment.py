from github.Repository import Repository

from control_repository.puppetfile import Puppetfile


class Environment:
    """
    This class represents a Puppet environment.

    :type name: string
    :param name: The name of the puppet environment.
    :type: github_repository: :class:`github.Repository.Repository`
    :param github_repository: The Github Repository object (from PyGithub)
    """

    def __init__(self, name: str, github_repository: Repository) -> None:
        self._name: str = name
        self._github_repository: Repository = github_repository

    @property
    def name(self) -> str:
        """
        :type: string
        """
        return self._name

    def get_puppetfile(self) -> Puppetfile:
        """
        Retrieve the puppetfile present in the current Puppet environment.

        :rtype: :class:`control_repository.puppetfile.Puppetfile`
        :return: A Puppet Puppetfile object
        """
        return Puppetfile.from_github_repository(self._github_repository,
                                                 self._name)
