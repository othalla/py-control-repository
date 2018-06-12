from ppfilemgr.exceptions import ModuleBadGitReferenceTypeExcption


class PuppetModule:
    def __init__(self, name: str) -> None:
        self._name = name

    @property
    def name(self):
        return self._name


class ForgeModule(PuppetModule):
    def __init__(self, name: str, version: str) -> None:
        super(ForgeModule, self).__init__(name)
        self._version = version

    @property
    def version(self):
        return self._version


class GitModule(PuppetModule):
    def __init__(self, name: str, url: str, git_ref_type: str,
                 git_ref: str) -> None:
        super(GitModule, self).__init__(name)
        self._url = url
        if git_ref_type not in ['ref', 'branch', 'tag', 'commit']:
            raise ModuleBadGitReferenceTypeExcption
        self._git_reference_type = git_ref_type
        self._git_reference = git_ref

    @property
    def git_url(self):
        return self._url

    @property
    def git_reference_type(self):
        return self._git_reference_type

    @property
    def git_reference(self):
        return self._git_reference
