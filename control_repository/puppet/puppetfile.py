from typing import List, Optional

from github import GithubException
from github.Repository import Repository

from control_repository.exceptions import PuppetfileNotFoundException
from control_repository.puppet_module import ForgeModule, GitModule


class Puppetfile:
    def __init__(self,
                 github_repository: Repository,
                 environment: str,
                 forge_modules: List[ForgeModule] = [],
                 git_modules: List[GitModule] = [],
                 forge_url: Optional[str] = None) -> None:
        self._github_repository: Repository = github_repository
        self._environment = environment
        self._forge_modules: List[ForgeModule] = forge_modules
        self._git_modules: List[GitModule] = git_modules
        self._forge_url: Optional[str] = forge_url

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
        for index, line in enumerate(splitted_content):
            if line.startswith('forge '):
                self._forge_url = line.split('\'')[1]
            if line.startswith('mod '):
                if not line.endswith(','):
                    self._forge_modules.append(ForgeModule.from_line(line))
                else:
                    count = 1
                    while splitted_content[index+count].endswith(','):
                        count += 1
                    module_lines = splitted_content[index:(index+count+1)]
                    git_module = GitModule.from_lines(module_lines)
                    self._git_modules.append(git_module)

    @classmethod
    def from_github_repository(cls,
                               github_repository: Repository,
                               environment: str) -> "Puppetfile":
        try:
            content = github_repository.get_file_contents('/Puppetfile',
                                                          ref=environment)
            decoded_content = content.decoded_content.decode('utf-8')
        except GithubException:
            raise PuppetfileNotFoundException
