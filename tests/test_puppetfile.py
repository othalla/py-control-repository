from control_repository.puppet_module import GitModule, ForgeModule
from control_repository.puppetfile import Puppetfile


class TestPuppetfile:
    def test_it_add_module(self):
        puppetfile = Puppetfile()
        module = GitModule('nginx', 'http://someurl/repo/nginx.git', 'tag',
                           'v0.0.1')
        puppetfile.add_module(module)

    def test_set_forge(self):
        puppetfile = Puppetfile()
        puppetfile.set_forge('https://forge.puppetlabs.com')
        assert puppetfile.forge_url == 'https://forge.puppetlabs.com'

    def test_to_string_with_forge_and_git_module(self):
        puppetfile = Puppetfile()
        puppetfile.add_module(GitModule('nginx',
                                        'http://someurl/repo/nginx.git',
                                        'tag', 'v0.0.1'))
        puppetfile.add_module(ForgeModule('puppetlabs/stdlib', '4.25.1'))
        expected_content = ("mod 'puppetlabs/stdlib', '4.25.1'\n"
                            "mod 'nginx',\n"
                            "  :git => 'http://someurl/repo/nginx.git',\n"
                            "  :tag => 'v0.0.1'\n")
        assert puppetfile.to_string() == expected_content

    def test_to_string_with_given_forge_url(self):
        puppetfile = Puppetfile()
        puppetfile.add_module(GitModule('nginx',
                                        'http://someurl/repo/nginx.git',
                                        'tag', 'v0.0.1'))
        puppetfile.add_module(ForgeModule('puppetlabs/stdlib', '4.25.1'))
        puppetfile.set_forge('http://url.forge.custom')
        expected_content = ("forge 'http://url.forge.custom'\n"
                            "mod 'puppetlabs/stdlib', '4.25.1'\n"
                            "mod 'nginx',\n"
                            "  :git => 'http://someurl/repo/nginx.git',\n"
                            "  :tag => 'v0.0.1'\n")
        assert puppetfile.to_string() == expected_content
