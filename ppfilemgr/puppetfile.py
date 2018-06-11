import re
from puppetfile.puppet_module import PuppetModule


class Puppetfile:
    def __init__(self):
        self._modules = []
        self._forge = None

    def add_module(self, module: PuppetModule):
        self._modules.append(module)

    def set_forge(self, url):
        self._forge_url = url
