from unittest.mock import MagicMock

import pytest
from github import GithubException

from control_repository.exceptions import PuppetfileNotFoundException
from control_repository.puppet_module import ForgeModule, GitModule
from control_repository.puppet.puppetfile import Puppetfile


class TestPuppetfile:
    @staticmethod
    def test_with_an_empty_puppetfile():
        github_repository = MagicMock()
        puppetfile = Puppetfile(github_repository, 'env')
        assert puppetfile.forge_modules == []
        assert puppetfile.git_modules == []
        assert puppetfile.forge_url is None

    @staticmethod
    def test_it_parse_forge_url():
        github_repository = MagicMock()
        puppetfile = Puppetfile(github_repository,
                                'env',
                                forge_url='https://forge.url')
        assert puppetfile.forge_modules == []
        assert puppetfile.git_modules == []
        assert puppetfile.forge_url == 'https://forge.url'

    @staticmethod
    def test_it_parse_a_forge_module():
        expected_module = ForgeModule('puppetlabs/apache', '0.1.10')
        github_repository = MagicMock()
        puppetfile = Puppetfile(github_repository,
                                'env',
                                forge_modules=[expected_module])
        assert expected_module in puppetfile.forge_modules

    @staticmethod
    def test_it_parse_a_git_module():
        expected_module = GitModule('apache',
                                    'https://url/git/apache',
                                    'ref',
                                    'ed19f')
        github_repository = MagicMock()
        puppetfile = Puppetfile(github_repository,
                                'env',
                                git_modules=[expected_module])
        assert expected_module in puppetfile.git_modules

    @staticmethod
    def test_it_parse_both_git_and_forge_modules():
        github_repository = MagicMock()
        git_module_apache = GitModule('apache',
                                      'https://url/git/apache',
                                      'ref',
                                      'ed19f')
        git_module_custommod = GitModule('custommod',
                                         'https://url/git/custommod')
        forge_module_apache = ForgeModule('puppetlabs/apache', '0.1.10')
        forge_module_vcsrepo = ForgeModule('puppetlabs/vcsrepo', '0.2.10')
        puppetfile = Puppetfile(github_repository,
                                'env',
                                forge_modules=[forge_module_apache,
                                               forge_module_vcsrepo],
                                git_modules=[git_module_apache,
                                             git_module_custommod])
        assert git_module_apache in puppetfile.git_modules
        assert git_module_custommod in puppetfile.git_modules
        assert forge_module_apache in puppetfile.forge_modules
        assert forge_module_vcsrepo in puppetfile.forge_modules


class TestPuppetfileFromGitubRepository:
    @staticmethod
    def test_it_read_and_decode_puppetfile_from_github_repository():
        github_repository = MagicMock()
        Puppetfile.from_github_repository(github_repository, 'env')
        github_repository.get_file_contents.assert_called_once_with(
            '/Puppetfile', ref='env')
        content = github_repository.get_file_contents()
        content.decoded_content.decode.assert_called_once_with('utf-8')

    @staticmethod
    def test_no_puppetfile_in_github_repository():
        github_repository = MagicMock()
        github_repository.get_file_contents.side_effect = GithubException(
            404, 'file not found')
        with pytest.raises(PuppetfileNotFoundException):
            Puppetfile.from_github_repository(github_repository, 'env')

    @staticmethod
    def test_it_return_a_puppetfile_with_forge_modules():
        github_repository = MagicMock()
        content = github_repository.get_file_contents()
        content.decoded_content.decode.return_value = (
            "mod 'apache',\n"
            "    :git => 'https://url/git/apache',\n"
            "    :ref => 'ed19f'\n"
            "mod 'custommod',\n"
            "    :git => 'https://url/git/custommod'\n"
            "mod 'puppetlabs/apache', '0.1.10'\n"
            "mod 'puppetlabs/vcsrepo', '0.2.10'"
        )
        forge_module_apache = ForgeModule('puppetlabs/apache', '0.1.10')
        forge_module_vcsrepo = ForgeModule('puppetlabs/vcsrepo', '0.2.10')
        git_module_apache = GitModule('apache',
                                      'https://url/git/apache',
                                      'ref',
                                      'ed19f')
        git_module_custommod = GitModule('custommod',
                                         'https://url/git/custommod')
        puppetfile = Puppetfile.from_github_repository(github_repository, 'env')
        assert forge_module_apache in puppetfile.forge_modules
        assert forge_module_vcsrepo in puppetfile.forge_modules
        assert git_module_apache in puppetfile.git_modules
        assert git_module_custommod in puppetfile.git_modules
