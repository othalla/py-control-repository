from unittest.mock import MagicMock

from control_repository.puppet_module import ForgeModule, GitModule
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

    @staticmethod
    def test_it_parse_a_git_module():
        puppetfile_content = ('mod "apache",\n'
                              '    :git => "https://url/git/apache",\n'
                              '    :ref => "ed19f"')
        expected_module = GitModule('apache',
                                    'https://url/git/apache',
                                    'ref',
                                    'ed19f')
        github_repository = MagicMock()
        puppetfile = Puppetfile(puppetfile_content, github_repository)
        assert expected_module in puppetfile.git_modules

    @staticmethod
    def test_it_parse_both_git_and_forge_modules():
        puppetfile_content = ('mod "apache",\n'
                              '    :git => "https://url/git/apache",\n'
                              '    :ref => "ed19f"\n'
                              'mod "custommod",\n'
                              '    :git => "https://url/git/custommod"\n'
                              'mod "puppetlabs/apache", "0.1.10"\n'
                              'mod "puppetlabs/vcsrepo", "0.2.10"'
                              )
        github_repository = MagicMock()
        puppetfile = Puppetfile(puppetfile_content, github_repository)
        git_module_apache = GitModule('apache',
                                      'https://url/git/apache',
                                      'ref',
                                      'ed19f')
        git_module_custommod = GitModule('custommod',
                                         'https://url/git/custommod')
        forge_module_apache = ForgeModule('puppetlabs/apache', '0.1.10')
        forge_module_vcsrepo = ForgeModule('puppetlabs/vcsrepo', '0.2.10')
        assert git_module_apache in puppetfile.git_modules
        assert git_module_custommod in puppetfile.git_modules
        assert forge_module_apache in puppetfile.forge_modules
        assert forge_module_vcsrepo in puppetfile.forge_modules


class TestPuppetfileFromGitubRepository:
    @staticmethod
    def test_():
        pass
