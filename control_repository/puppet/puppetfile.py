from typing import List

from github.Repository import Repository

from control_repository.puppet_module import ForgeModule, GitModule


class Puppetfile:
    def __init__(self, content: str, github_repository: Repository) -> None:
        self._content: str = content.replace('"', "'")
        self._github_repository: Repository = github_repository
        self._forge_modules: List[ForgeModule] = []
        self._git_modules: List[GitModule] = []
        self._forge_url: str = ''
        self._parse()

    @property
    def forge_modules(self) -> List[ForgeModule]:
        return self._forge_modules

    @property
    def git_modules(self) -> List[GitModule]:
        return self._git_modules

    @property
    def forge_url(self) -> str:
        return self._forge_url

    def _parse(self) -> None:
        splitted_content = self._content.split('\n')
        for line in splitted_content:
            if line.startswith('forge '):
                self._forge_url = line.split('\'')[1]
            elif line.startswith('mod '):
                self._forge_modules.append(ForgeModule.from_line(line))
