from unittest.mock import MagicMock

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
