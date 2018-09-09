from github import Repository

class Environment:
    def __init__(self, name: str, github_repository: Repository) -> None:
        self._name = name
        self._github_repository = github_repository
