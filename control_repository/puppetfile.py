from typing import List, Optional, Tuple

from github import GithubException
from github.Repository import Repository

from control_repository.exceptions import (PuppetfileNotFoundException,
                                           PuppetfileUpdateException,
                                           ModuleAlreadyPresentException,
                                           ModuleNotFoundException)
from control_repository.puppet_module import ForgeModule, GitModule


class Puppetfile:
    """
    This class represents a Puppetfile

    :type github_repository: :class:`github.Repository.Repository`
    :param github_repository: The PyGithub Repository object.
    :type environment: string
    :param environment: The name of the Puppet environment.
    :type sha: string
    :param sha: The git file sha of the Puppetfile.
    :type forge_modules: list of
                         :class:`control_repository.puppet_module.ForgeModule`
    :param forge_modules: A list of Puppet forge modules.
    :type git_modules: list of
                       :class:`control_repository.puppet_module.GitModule`
    :param git_modules: A list of Puppet git modules.
    :type sha: string
    :param sha: The url of the Puppet forge used to download modules.
    """

    def __init__(self,
                 github_repository: Repository,
                 environment: str,
                 sha: Optional[str] = None,
                 forge_modules: Optional[List[ForgeModule]] = None,
                 git_modules: Optional[List[GitModule]] = None,
                 forge_url: Optional[str] = None) -> None:
        self._github_repository: Repository = github_repository
        self._environment = environment
        self._sha: Optional[str] = sha
        self._forge_modules: List[ForgeModule]
        self._forge_modules = [] if forge_modules is None else forge_modules
        self._git_modules: List[GitModule]
        self._git_modules = [] if git_modules is None else git_modules
        self._forge_url: Optional[str] = forge_url

    @property
    def sha(self) -> Optional[str]:
        """
        :type: string
        """
        return self._sha

    @property
    def forge_modules(self) -> List[ForgeModule]:
        """
        :type: list of :class:`control_repository.puppet_module.ForgeModule`
        """
        return self._forge_modules

    @property
    def git_modules(self) -> List[GitModule]:
        """
        :type: list of :class:`control_repository.puppet_module.GitModule`
        """
        return self._git_modules

    @property
    def forge_url(self) -> Optional[str]:
        """
        :type: string
        """
        return self._forge_url

    def list_modules(self) -> Optional[List[str]]:
        """
        List all Puppet git and forge modules names present in the Puppetfile.

        :rtype: None or list of string
        :return: The list of Puppet modules in the Puppetfile.
        """
        module_list: List[str] = []
        for forge_module in self._forge_modules:
            module_list.append(forge_module.name)
        for git_module in self._git_modules:
            module_list.append(git_module.name)
        return module_list

    def set_forge_url(self, url: str) -> None:
        """
        Set the url used to download Puppet forge modules.

        :type: string
        :param: The url of the Puppet forge.
        """
        self._forge_url = url
        self._update_file_on_github('forge URL')

    def remove_forge_url(self) -> None:
        """
        Remove the url used to download Puppet forge modules.
        """
        self._forge_url = None
        self._update_file_on_github('- Remove forge URL')

    def add_git_module(self,
                       name: str,
                       url: str,
                       reference_type: Optional[str] = None,
                       reference: Optional[str] = None) -> None:
        module = GitModule(name, url, reference_type=reference_type,
                           reference=reference)
        for module in self._git_modules:
            if name == module.name:
                raise ModuleAlreadyPresentException
        self._git_modules.append(module)
        self._update_file_on_github(f'- Update git module {name}')

    def add_forge_module(self,
                         name: str,
                         version: Optional[str] = None) -> None:
        module = ForgeModule(name, version=version)
        for module in self._forge_modules:
            if name == module.name:
                raise ModuleAlreadyPresentException
        self._forge_modules.append(module)
        self._update_file_on_github(f'- Add forge module {name}')

    def update_git_module(self, name: str,
                          reference: str,
                          reference_type: Optional[str] = None) -> None:
        for module in self._git_modules:
            if name == module.name:
                module.set_reference(reference,
                                     reference_type=reference_type)
                return self._update_file_on_github(
                    f'- Update git module {name}')
        raise ModuleNotFoundException

    def update_forge_module(self, name: str, version: str) -> None:
        for module in self._forge_modules:
            if name == module.name:
                module.set_version(version)
                return self._update_file_on_github(
                    f'- Update forge module {name}')
        raise ModuleNotFoundException

    def _update_file_on_github(self, source: str) -> None:
        try:
            update_result = self._github_repository.update_file(
                "/Puppetfile",
                f'Update Puppetfile {source}',
                str(self),
                self._sha)
        except GithubException:
            raise PuppetfileUpdateException
        self._sha = update_result['content'].sha

    def __str__(self) -> str:
        content: str = ''
        if self.forge_url:
            content = f"forge '{self._forge_url}'"
        if self.forge_modules:
            for forge_module in self._forge_modules:
                content += str(forge_module)
        if self._git_modules:
            for git_module in self._git_modules:
                content += str(git_module)
        return content

    @classmethod
    def from_github_repository(cls,
                               github_repository: Repository,
                               environment: str) -> "Puppetfile":
        decoded_content, file_sha = cls._get_file_content_from_repository(
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
                    while splitted_content[index + count].endswith(','):
                        count += 1
                    module_lines = splitted_content[index:(index + count + 1)]
                    git_module = GitModule.from_lines(module_lines)
                    git_modules.append(git_module)
        return cls(github_repository,
                   environment,
                   sha=file_sha,
                   forge_modules=forge_modules,
                   git_modules=git_modules,
                   forge_url=forge_url)

    @staticmethod
    def _get_file_content_from_repository(github_repository: Repository,
                                          environment: str) -> Tuple[str, str]:
        try:
            content = github_repository.get_file_contents('/Puppetfile',
                                                          ref=environment)
            return content.decoded_content.decode('utf-8'), content.sha
        except GithubException:
            raise PuppetfileNotFoundException
