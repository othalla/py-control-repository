from enum import Enum
from typing import Any, List, Optional

from control_repository.exceptions import (ModuleParserException,
                                           ModuleMalformedException)


class GitReferenceType(Enum):
    REF = 'ref'
    COMMIT = 'commit'
    BRANCH = 'branch'
    TAG = 'tag'

    @classmethod
    def has_value(cls, value: str) -> None:
        if value not in cls.values():
            raise AttributeError

    @classmethod
    def values(cls) -> List[str]:
        return [reference_type.value for reference_type in cls]


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
                 reference_type: Optional[str] = None,
                 reference: Optional[str] = None) -> None:
        super(GitModule, self).__init__(name)
        self._url: str = url
        if reference_type and not reference:
            raise ModuleMalformedException
        if reference_type:
            GitReferenceType.has_value(reference_type)
        self._reference_type: Optional[str] = reference_type
        self._reference: Optional[str] = reference

    @property
    def git_url(self) -> str:
        return self._url

    @property
    def git_reference_type(self) -> Optional[str]:
        return self._reference_type

    @property
    def git_reference(self) -> Optional[str]:
        return self._reference

    def set_reference(self,
                      reference: str,
                      reference_type: Optional[str] = None) -> None:
        if reference_type:
            self._reference_type = reference_type
        self._reference = reference

    def __str__(self) -> str:
        if self._reference and self._reference_type:
            return (
                f"mod '{self._name}',\n"
                f"  :git => '{self._url}',\n"
                f"  :{self._reference_type} => '{self._reference}'"
            )
        return (
            f"mod '{self._name}',\n"
            f"  :git => '{self._url}'"
        )

    @classmethod
    def from_lines(cls, lines: List[str]) -> "GitModule":
        reference: Optional[str] = None
        reference_type: Optional[str] = None
        url: str = ''
        for line in lines:
            if line.startswith('mod'):
                name = line.split("'")[1]
            elif ':git' in line:
                url = line.split("'")[1]
            else:
                for allowed_reference in GitReferenceType.values():
                    if allowed_reference in line:
                        reference_type = allowed_reference
                        break
                if reference_type:
                    reference = line.split("'")[1]
        if not url:
            raise ModuleParserException
        return cls(name,
                   url,
                   reference_type=reference_type,
                   reference=reference)
