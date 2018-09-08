from github import Github

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

    def get_environment(self, environment):
        return Environment()
