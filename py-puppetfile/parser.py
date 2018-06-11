import re


class PuppetModule:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


class Puppetfile:
    def __init__(self):
        self._modules = []
        self._forge = None

    def add_module(self, module: PuppetModule):
        self._modules.append(module)

    def set_forge(self, url):
        self._forge_url = url



class ForgeModule(PuppetModule):
    def __init__(self, name, version):
        self._name = name
        self._version = version


class GitModule(PuppetModule):
    def __init__(self, name, url, git_reference_type, git_reference):
        self._name = name
        self._url = url
        self._git_reference_type = git_reference_type
        self._git_reference = git_reference


# with open('Puppetfile', 'r') as ppfile:
    # for line in ppfile:
        # print('this line : ' + line)
        # if line.startswith('forge'):
            # print('Forge directive')
        # if line.startswith('mod'):
            # print('python module')
            # if line.endswith(',\n'):
                # print('GitUrlModule')
                # # print(re.search(' (.*),', line))
                # module = line.split('\'')[1]
                # ppmodule = PuppetModule(module)
                # print(ppmodule.name)
                # # print(ppfile.next())
            # else:
                # print('ForgeModule')
        # if line.sta


def file_to_list():
    with open('Puppetfile', 'r') as ppfile:
        file_to_list = ppfile.read().split('\n')
        return file_to_list

splited_file = file_to_list()

for index, fragment in enumerate(splited_file):
    # print(fragment.index())
    if fragment.startswith('forge'):
        print('Forge directive')
    elif fragment.startswith('mod'):
        print('python module')
        if fragment.endswith(','):
            print('GitUrlModule')
            print(fragment.split('\'')[1])  # URL MOD NAME
            next_line = splited_file[index + 1]  # REF
            if next_line.startswith('  :'):
                # print(next_line)
                next_line_splited = re.split('  :|\'| ',next_line)
                version = next_line_splited[1]
                url = next_line_splited[4]
                print(version)
                print(url)
        else:
            print('ForgeModule')
            print(fragment.split('\'')[1])  # URL MOD NAME



