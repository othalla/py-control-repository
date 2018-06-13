import re
from ppfilemgr.puppetfile import Puppetfile


class ForgeModule:
    def __init__(self, name, version):
        self._name = name
        self._version = version

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    def __eq__(self, comp):
        if self.__dict__ == comp.__dict__:
            return True
        return False

class GitModule:
    def __init__(self, name, url, ref_type, ref):
        self._name = name
        self._url = url
        self._ref_type = ref_type
        self._ref = ref

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url

    def __eq__(self, comp):
        if self.__dict__ == comp.__dict__:
            return True
        return False


def string_to_puppetfile(content: str):
    puppetfile = Puppetfile()
    splited_content = content.split('\n')

    for index, fragment in enumerate(splited_content):
        if fragment.startswith('forge '):
            puppetfile.set_forge(fragment.split('\'')[1])
        if fragment.startswith('mod '):
            module = None
            if fragment.endswith(','):
                module = generate_git_module(splited_content[index:index + 3])
            else:
                module = generate_forge_module(fragment)
            puppetfile.add_module(module)
    return puppetfile


def generate_forge_module(line):
    parts = line.split('\'')
    name = parts[1]
    version = parts[3]
    return ForgeModule(name, version)


def generate_git_module(lines):
    name = lines[0].split('\'')[1]
    for line in lines[1:]:
        if line.startswith('  :git'):
            url = line.split('\'')[1]
        if line.startswith(('  :tag', '  :ref', '  :commit', '  :branch')):
            ref_type = re.split('  :| |\'', line)[1]
            ref = re.split('  :| |\'', line)[4]
    return GitModule(name, url, ref_type, ref)
