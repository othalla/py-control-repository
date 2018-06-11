class PuppetModule:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


class Puppetfile:
    def __init__(self):
        self._modules = []
        self._forge_url = None

    def add_module(self, module: PuppetModule):
        self._modules.append(module)

    def set_forge(self, url):
        self._forge_url = url



class ForgeModule(PuppetModule):
    def __init__(self, name, version):
        super(ForgeModule, self).__init__(name)
        self._version = version


class GitModule(PuppetModule):
    def __init__(self, name, url, git_reference_type, git_reference):
        super(GitModule, self).__init__(name)
        self._url = url
        self._git_reference_type = git_reference_type
        self._git_reference = git_reference
