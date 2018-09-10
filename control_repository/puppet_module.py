from typing import Any

from control_repository.exceptions import ModuleBadGitReferenceTypeExcption


class PuppetModule:
    def __init__(self, name: str) -> None:
        self._name: str = name

    def __eq__(self, compared: Any) -> bool:
        if self.__dict__ == compared.__dict__:
            return True
        return False

    @property
    def name(self) -> str:
        return self._name


class ForgeModule(PuppetModule):
    def __init__(self, name: str, version: str = '') -> None:
        super(ForgeModule, self).__init__(name)
        self._version: str = version

    @property
    def version(self) -> str:
        return self._version


class GitModule(PuppetModule):
    def __init__(self, name: str, url: str, git_ref_type: str,
                 git_ref: str) -> None:
        super(GitModule, self).__init__(name)
        self._url: str = url
        if git_ref_type not in ['ref', 'branch', 'tag', 'commit']:
            raise ModuleBadGitReferenceTypeExcption
        self._git_reference_type: str = git_ref_type
        self._git_reference: str = git_ref

    @property
    def git_url(self) -> str:
        return self._url

    @property
    def git_reference_type(self) -> str:
        return self._git_reference_type

    @property
    def git_reference(self) -> str:
        return self._git_reference
