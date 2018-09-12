from unittest.mock import MagicMock

from control_repository.puppet_module import ForgeModule
from control_repository.puppet.puppetfile import Puppetfile


class TestPuppetfile:
    @staticmethod
    def test_with_an_empty_puppetfile():
        github_repository = MagicMock()
        puppetfile = Puppetfile('', github_repository)
        assert puppetfile.forge_modules == []
        assert puppetfile.git_modules == []
        assert puppetfile.forge_url == ''

    @staticmethod
    def test_it_parse_forge_url():
        github_repository = MagicMock()
        puppetfile = Puppetfile('forge "https://forge.url"', github_repository)
        assert puppetfile.forge_modules == []
        assert puppetfile.git_modules == []
        assert puppetfile.forge_url == 'https://forge.url'

    @staticmethod
    def test_it_parse_a_forge_module():
        puppetfile_content = ('mod "puppetlabs/apache", "0.1.10"')
        expected_module = ForgeModule('puppetlabs/apache', '0.1.10')
        github_repository = MagicMock()
        puppetfile = Puppetfile(puppetfile_content, github_repository)
        assert expected_module in puppetfile.forge_modules
