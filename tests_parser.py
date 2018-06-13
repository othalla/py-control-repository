from parser import string_to_puppetfile
from parser import ForgeModule, GitModule


class TestStringToPuppetfile:
    def test_it_add_forge(self):
        string = "forge 'forgeurl.com'"
        puppetfile = string_to_puppetfile(string)
        assert puppetfile.forge_url == 'forgeurl.com'

    def test_it_add_forge_module(self):
        string = "mod 'nginx', '1.1.8'"
        puppetfile = string_to_puppetfile(string)
        nginx_module = ForgeModule('nginx', '1.1.8')
        assert nginx_module in puppetfile.modules

    def test_it_add_giturl_module(self):
        string = ("mod 'custom',\n"
                  "  :git => 'giturl.com',\n"
                  "  :tag => '1.1.8'")
        puppetfile = string_to_puppetfile(string)
        custom_module = GitModule('custom', 'giturl.com', 'tag', '1.1.8')
        assert custom_module in puppetfile.modules

    def test_it_add_forge_url_forge_module_git_module(self):
        string = ("forge 'forge.url'\n"
                  "mod 'nginx', '0.1.1'\n"
                  "mod 'stdlib', '1.5.1'\n"
                  "mod 'custom',\n"
                  "  :git => 'giturl.com',\n"
                  "  :tag => '1.1.8'\n"
                  "mod 'another',\n"
                  "  :git => 'another.com',\n"
                  "  :tag => '1.0.0'")
        puppetfile = string_to_puppetfile(string)

        custom_module = GitModule('custom', 'giturl.com', 'tag', '1.1.8')
        another_module = GitModule('another', 'another.com', 'tag', '1.0.0')
        nginx_module = ForgeModule('nginx', '0.1.1')
        stdlib_module = ForgeModule('stdlib', '1.5.1')

        assert puppetfile.forge_url == 'forge.url'
        assert custom_module in puppetfile.modules
        assert another_module in puppetfile.modules
        assert nginx_module in puppetfile.modules
        assert stdlib_module in puppetfile.modules
