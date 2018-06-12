from ppfilemgr.puppet_module import GitModule, ForgeModule
from ppfilemgr.puppetfile import Puppetfile


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

    def test_content_returns_correct_file(self):
        puppetfile = Puppetfile()
        puppetfile.add_module(GitModule('nginx',
                                        'http://someurl/repo/nginx.git',
                                        'tag', 'v0.0.1'))
        puppetfile.add_module(ForgeModule('puppetlabs/stdlib', '4.25.1'))
        expected_content = ("mod 'nginx',\n"
                            "  :git => 'http://someurl/repo/nginx.git',\n"
                            "  :tag => 'v0.0.1'\n"
                            "mod 'puppetlabs/stdlib', '4.25.1'\n")
        assert puppetfile.generate() == expected_content
