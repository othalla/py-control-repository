import re
from control_repository.puppet_module import PuppetModule, ForgeModule, GitModule


class Puppetfile:
    def __init__(self) -> None:
        self._modules = []
        self._forge_url = None

    def add_module(self, module: PuppetModule) -> None:
        self._modules.append(module)

    def update_module(self, updated_module):
        for index, module in enumerate(self._modules):
            if module.name == updated_module.name:
                self._modules[index] = updated_module

    def set_forge(self, url) -> None:
        self._forge_url = url

    @property
    def forge_url(self):
        return self._forge_url

    @property
    def modules(self):
        return self._modules

    def to_string(self):
        content = "{}".format(self._write_forge_url_header())
        content = "{}{}".format(content, self._write_forge_modules())
        content = "{}{}".format(content, self._write_git_modules())
        return content

    def _write_forge_url_header(self):
        if self._forge_url is not None:
            return "forge '{}'\n".format(self._forge_url)
        return ""

    def _write_forge_modules(self):
        fragment = ""
        for module in self._modules:
            if isinstance(module, ForgeModule):
                fragment = "{}mod '{}', '{}'\n".format(fragment,
                                                       module.name,
                                                       module.version)
        return fragment

    def _write_git_modules(self):
        fragment = ""
        for module in self._modules:
            if isinstance(module, GitModule):
                fragment = "{}mod '{}',\n".format(fragment, module.name)
                fragment = "{}  :git => '{}',\n".format(fragment,
                                                        module.git_url)
                fragment = "{}  :{} => '{}'\n".format(
                    fragment, module.git_reference_type, module.git_reference)
        return fragment