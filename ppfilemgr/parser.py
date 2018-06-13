import re

def parse_puppetfile(puppetfile):
    pass



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

