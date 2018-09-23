from typing import List, Optional, Tuple

from github import GithubException
from github.Repository import Repository

from control_repository.exceptions import PuppetfileNotFoundException
from control_repository.puppet_module import ForgeModule, GitModule


class Puppetfile:
    def __init__(self,
                 github_repository: Repository,
                 environment: str,
                 sha: Optional[str] = None,
                 forge_modules: List[ForgeModule] = [],
                 git_modules: List[GitModule] = [],
                 forge_url: Optional[str] = None) -> None:
        self._github_repository: Repository = github_repository
        self._environment = environment
        self._sha: Optional[str] = sha
        self._forge_modules: List[ForgeModule] = forge_modules
        self._git_modules: List[GitModule] = git_modules
        self._forge_url: Optional[str] = forge_url

    @property
    def sha(self) -> Optional[str]:
        return self._sha

    @property
    def forge_modules(self) -> List[ForgeModule]:
        return self._forge_modules

    @property
    def git_modules(self) -> List[GitModule]:
        return self._git_modules

    @property
    def forge_url(self) -> Optional[str]:
        return self._forge_url

    def set_forge_url(self, url: str) -> None:
        self._forge_url = url
        self._update_file_on_github('forge URL')

    def _update_file_on_github(self, source: str) -> None:
        new_content = self._to_string()
        self._github_repository.update_file("/Puppetfile",
                                            f'Update Puppetfile {source}',
                                            new_content,
                                            self._sha)

    def _to_string(self) -> str:
        content: str = ''
        if self.forge_url:
            content = f"forge '{self._forge_url}'"
        return content

    @classmethod
    def from_github_repository(cls,
                               github_repository: Repository,
                               environment: str) -> "Puppetfile":
        decoded_content, file_sha = _get_file_content_from_repository(
            github_repository, environment)
        forge_url = None
        forge_modules = []
        git_modules = []
        splitted_content = decoded_content.split('\n')
        for index, line in enumerate(splitted_content):
            if line.startswith('forge '):
                forge_url = line.split('\'')[1]
            if line.startswith('mod '):
                if not line.endswith(','):
                    forge_modules.append(ForgeModule.from_line(line))
                else:
                    count = 1
                    while splitted_content[index+count].endswith(','):
                        count += 1
                    module_lines = splitted_content[index:(index+count+1)]
                    git_module = GitModule.from_lines(module_lines)
                    git_modules.append(git_module)
        return cls(github_repository,
                   environment,
                   sha=file_sha,
                   forge_modules=forge_modules,
                   git_modules=git_modules,
                   forge_url=forge_url)


def _get_file_content_from_repository(github_repository: Repository,
                                      environment: str) -> Tuple[str, str]:
    try:
        content = github_repository.get_file_contents('/Puppetfile',
                                                      ref=environment)
        return content.decoded_content.decode('utf-8'), content.sha
    except GithubException:
        raise PuppetfileNotFoundException
