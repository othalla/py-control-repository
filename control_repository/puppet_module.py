from typing import Any, List, Optional

from control_repository.exceptions import (ModuleBadGitReferenceTypeExcption,
                                           ModuleParserException)


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
    def __init__(self, name: str, version: Optional[str] = None) -> None:
        super(ForgeModule, self).__init__(name)
        self._version: Optional[str] = version

    @property
    def version(self) -> Optional[str]:
        return self._version

    def __str__(self) -> str:
        if self._version:
            return f"mod '{self._name}', '{self._version}'"
        return f"mod '{self._name}'"

    def set_version(self, version: str) -> None:
        self._version = version

    @classmethod
    def from_line(cls, line: str) -> "ForgeModule":
        fragments = line.split("'")
        if len(fragments) == 3:
            if line.endswith(', :latest'):
                return ForgeModule(fragments[1], version=':latest')
            return ForgeModule(fragments[1])
        if len(fragments) == 5:
            return ForgeModule(fragments[1], version=fragments[3])
        raise ModuleParserException


class GitModule(PuppetModule):
    def __init__(self,
                 name: str,
                 url: str,
                 git_reference_type: str = '',
                 git_reference: str = '') -> None:
        super(GitModule, self).__init__(name)
        self._url: str = url
        if git_reference_type not in ['', 'ref', 'branch', 'tag', 'commit']:
            raise ModuleBadGitReferenceTypeExcption
        self._git_reference_type: str = git_reference_type
        self._git_reference: str = git_reference

    @property
    def git_url(self) -> str:
        return self._url

    @property
    def git_reference_type(self) -> str:
        return self._git_reference_type

    @property
    def git_reference(self) -> str:
        return self._git_reference

    @classmethod
    def from_lines(cls, lines: List[str]) -> "GitModule":
        allowed_references: List[str] = [':ref', ':branch', ':tag', ':commit']
        reference: str = ''
        reference_type: str = ''
        url: str = ''
        for line in lines:
            if line.startswith('mod'):
                name = line.split("'")[1]
            elif ':git' in line:
                url = line.split("'")[1]
            else:
                for allowed_reference in allowed_references:
                    if allowed_reference in line:
                        reference_type = allowed_reference
                        break
                if reference_type:
                    reference = line.split("'")[1]
        if not url:
            raise ModuleParserException
        return GitModule(name, url, git_reference_type=reference_type[1:],
                         git_reference=reference)
