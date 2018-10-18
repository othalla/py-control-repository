from typing import List, Optional, Tuple

from github import GithubException
from github.Repository import Repository

from control_repository.exceptions import (PuppetfileNotFoundException,
                                           ModuleAlreadyPresentException,
                                           ModuleNotFoundException)
from control_repository.modules import ForgeModule, GitModule


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
                         :class:`control_repository.modules.ForgeModule`
    :param forge_modules: A list of Puppet forge modules.
    :type git_modules: list of :class:`control_repository.modules.GitModule`
    :param git_modules: A list of Puppet git modules.
    """

    def __init__(self,
                 github_repository: Repository,
                 environment: str,
                 sha: Optional[str] = None,
                 forge_modules: Optional[List[ForgeModule]] = None,
                 git_modules: Optional[List[GitModule]] = None) -> None:
        self._github_repository: Repository = github_repository
        self._environment = environment
        self._sha: Optional[str] = sha
        self._forge_modules: List[ForgeModule]
        self._forge_modules = [] if forge_modules is None else forge_modules
        self._git_modules: List[GitModule]
        self._git_modules = [] if git_modules is None else git_modules

    @property
    def sha(self) -> Optional[str]:
        """
        :type: string
        """
        return self._sha

    @property
    def forge_modules(self) -> List[ForgeModule]:
        """
        :type: list of :class:`control_repository.modules.ForgeModule`
        """
        return self._forge_modules

    @property
    def git_modules(self) -> List[GitModule]:
        """
        :type: list of :class:`control_repository.modules.GitModule`
        """
        return self._git_modules

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

    def add_git_module(self,
                       name: str,
                       url: str,
                       reference_type: Optional[str] = None,
                       reference: Optional[str] = None) -> None:
        """
        Add a Puppet git module to the Puppetfile.

        :type name: string
        :param name: The name of the Puppet git module to add to the
                     Puppetfile.
        :type url: string
        :param url: The git URL of the Puppet git module to add to the
                    Puppetfile.
        :type reference_type: string
        :param reference_type: The git reference type (ref, commit, branch,
                               tag) of the Puppet git module to add to the
                               Puppetfile.
        :type reference: string
        :param reference: The git reference of the Puppet git module to
                          add to the Puppetfile.
        """
        module = GitModule(name, url, reference_type=reference_type,
                           reference=reference)
        for module in self._git_modules:
            if name == module.name:
                raise ModuleAlreadyPresentException
        self._git_modules.append(module)
        self._update_file_on_github(f'Add git module {name}')

    def add_forge_module(self,
                         name: str,
                         version: Optional[str] = None) -> None:
        """
        Add a Puppet forge module to the Puppetfile.

        :type name: string
        :param name: The name of the Puppet forge module to add to the
                     Puppetfile.
        :type version: string
        :param version: The version of the Puppet forge module to add to the
                        Puppetfile.
        """
        module = ForgeModule(name, version=version)
        for module in self._forge_modules:
            if name == module.name:
                raise ModuleAlreadyPresentException
        self._forge_modules.append(module)
        self._update_file_on_github(f'Add forge module {name}')

    def remove_git_module(self,
                          name: str) -> None:
        """
        Remove a Puppet git module from the Puppetfile.

        :type name: string
        :param name: The name of the Puppet git module to remove from the
                     Puppetfile.
        """
        for git_module in self._git_modules:
            if git_module.name == name:
                return self.git_modules.remove(git_module)
        raise ModuleNotFoundException

    def remove_forge_module(self,
                            name: str) -> None:
        """
        Remove a Puppet forge module from the Puppetfile.

        :type name: string
        :param name: The name of the Puppet forge module to remove from the
                     Puppetfile.
        """
        for forge_module in self._forge_modules:
            if forge_module.name == name:
                return self._forge_modules.remove(forge_module)
        raise ModuleNotFoundException

    def update_git_module(self, name: str,
                          reference: str,
                          reference_type: Optional[str] = None) -> None:
        """
        Update an existing Puppet git module preset in the Puppetfile.

        :type name: string
        :param name: The name of the Puppet git module to update in the
                     Puppetfile.
        :type reference: string
        :param reference: The git reference of the Puppet git module to
                          update in the Puppetfile.
        :type reference_type: string
        :param reference_type: The git reference type (ref, commit, branch,
                               tag) of the Puppet git module to update in the
                               Puppetfile.
        """
        for module in self._git_modules:
            if name == module.name:
                commit_message = (f'Update git module {name} from '
                                  f'{module.reference} to {reference}')
                module.set_reference(reference,
                                     reference_type=reference_type)
                return self._update_file_on_github(commit_message)
        raise ModuleNotFoundException

    def update_forge_module(self, name: str, version: str) -> None:
        """
        Update an existing Puppet forge module present in the Puppetfile.

        :type name: string
        :param name: The name of the Puppet forge module to update in the
                     Puppetfile.
        :type version: string
        :param version: The version of the Puppet forge module to update in the
                        Puppetfile.
        """
        for module in self._forge_modules:
            if name == module.name:
                commit_message = (f'Update forge module {name} from '
                                  f'{module.version} to {version}')
                module.set_version(version)
                return self._update_file_on_github(commit_message)
        raise ModuleNotFoundException

    def _update_file_on_github(self, source: str) -> None:
        update_result = self._github_repository.update_file(
            "/Puppetfile",
            f'Puppetfile - {source}',
            str(self),
            self._sha)
        self._sha = update_result['content'].sha

    def __str__(self) -> str:
        content: str = ''
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
        splitted_content = decoded_content.replace('"', "'").split('\n')
        forge_modules, git_modules = cls._parse_puppet_modules(
            splitted_content)
        return cls(github_repository,
                   environment,
                   sha=file_sha,
                   forge_modules=forge_modules,
                   git_modules=git_modules)

    @staticmethod
    def _parse_puppet_modules(lines: List[str]) -> Tuple[List[ForgeModule],
                                                         List[GitModule]]:
        forge_modules = []
        git_modules = []
        for index, line in enumerate(lines):
            if line.startswith('mod '):
                if not line.endswith(','):
                    forge_modules.append(ForgeModule.from_line(line))
                else:
                    count = 1
                    while lines[index + count].endswith(','):
                        count += 1
                    module_lines = lines[index:(index + count + 1)]
                    git_module = GitModule.from_lines(module_lines)
                    git_modules.append(git_module)
        return forge_modules, git_modules

    @staticmethod
    def _get_file_content_from_repository(github_repository: Repository,
                                          environment: str) -> Tuple[str, str]:
        try:
            content = github_repository.get_file_contents('/Puppetfile',
                                                          ref=environment)
            return content.decoded_content.decode('utf-8'), content.sha
        except GithubException:
            raise PuppetfileNotFoundException
