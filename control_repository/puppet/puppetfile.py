from typing import List

from github.Repository import Repository

from control_repository.puppet_module import ForgeModule, GitModule


class Puppetfile:
    def __init__(self, content: str, github_repository: Repository) -> None:
        self._content: str = content
        self._github_repository: Repository = github_repository
        self._forge_modules: List[ForgeModule] = []
        self._git_modules: List[GitModule] = []
        self._forge_url: str = ''

    @property
    def forge_modules(self) -> ForgeModule:
        return self._forge_modules

    @property
    def git_modules(self) -> GitModule:
        return self._git_modules

    @property
    def forge_url(self) -> str:
        return self._forge_url
