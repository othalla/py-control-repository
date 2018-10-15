from copy import deepcopy
from unittest.mock import MagicMock

import pytest
from github import GithubException

from control_repository.exceptions import (PuppetfileNotFoundException,
                                           ModuleAlreadyPresentException,
                                           ModuleNotFoundException)
from control_repository.modules import ForgeModule, GitModule
from control_repository.puppetfile import Puppetfile


GIT_MODULE_APACHE = GitModule('apache',
                              'https://url/git/apache',
                              'ref',
                              'ed19f')


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
    def test_whith_no_puppetfile_in_github_repository():
        github_repository = MagicMock()
        github_repository.get_file_contents.side_effect = GithubException(
            404, 'file not found')
        with pytest.raises(PuppetfileNotFoundException):
            Puppetfile.from_github_repository(github_repository, 'env')

    @staticmethod
    def test_it_set_file_sha():
        github_repository = MagicMock()
        github_repository.get_file_contents().sha = 'shasha'
        puppetfile = Puppetfile.from_github_repository(github_repository, 'env')
        assert puppetfile.sha == 'shasha'

    @staticmethod
    def test_it_returns_a_puppetfile_with_both_git_and_forge_modules():
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
        git_module_custommod = GitModule('custommod',
                                         'https://url/git/custommod')
        puppetfile = Puppetfile.from_github_repository(github_repository, 'env')
        assert forge_module_apache in puppetfile.forge_modules
        assert forge_module_vcsrepo in puppetfile.forge_modules
        assert GIT_MODULE_APACHE in puppetfile.git_modules
        assert git_module_custommod in puppetfile.git_modules

    @staticmethod
    def test_it_parse_modules_with_both_simple_and_double_quotes():
        github_repository = MagicMock()
        content = github_repository.get_file_contents()
        content.decoded_content.decode.return_value = (
            "mod \"custommod\",\n"
            "    :git => \"https://url/git/custommod\"\n"
            "mod 'puppetlabs/apache', '0.1.10'\n"
            "mod \"puppetlabs/vcsrepo\", \"0.2.10\""
        )
        forge_module_apache = ForgeModule('puppetlabs/apache', '0.1.10')
        forge_module_vcsrepo = ForgeModule('puppetlabs/vcsrepo', '0.2.10')
        git_module_custommod = GitModule('custommod',
                                         'https://url/git/custommod')
        puppetfile = Puppetfile.from_github_repository(github_repository, 'env')
        assert forge_module_apache in puppetfile.forge_modules
        assert forge_module_vcsrepo in puppetfile.forge_modules
        assert git_module_custommod in puppetfile.git_modules


class TestPuppetfileAddGitModule:
    @staticmethod
    def test_it_add_a_git_module_to_the_puppetfile():
        github_repository = MagicMock()
        content = github_repository.get_file_contents()
        content.decoded_content.decode.return_value = ('')
        puppetfile = Puppetfile(github_repository, 'env', sha='shasha')
        assert puppetfile.git_modules == []
        puppetfile.add_git_module('apache',
                                  'https://url/git/apache',
                                  reference_type='ref',
                                  reference='ed19f')
        assert GIT_MODULE_APACHE in puppetfile.git_modules
        github_repository.update_file.assert_called_once_with(
            "/Puppetfile",
            "Puppetfile - Add git module apache",
            ("mod 'apache',\n"
             "  :git => 'https://url/git/apache',\n"
             "  :ref => 'ed19f'\n"),
            "shasha")

    @staticmethod
    def test_it_cannot_add_an_existing_git_module():
        github_repository = MagicMock()
        content = github_repository.get_file_contents()
        content.decoded_content.decode.return_value = ('')
        puppetfile = Puppetfile(github_repository,
                                'env',
                                sha='shasha',
                                git_modules=[GIT_MODULE_APACHE])
        with pytest.raises(ModuleAlreadyPresentException):
            puppetfile.add_git_module('apache', 'https://url/git/apache')


class TestPuppetfileAddForgeModule:
    @staticmethod
    def test_it_add_a_module_to_the_puppetfile():
        github_repository = MagicMock()
        content = github_repository.get_file_contents()
        content.decoded_content.decode.return_value = ('')
        puppetfile = Puppetfile(github_repository, 'env', sha='shasha')
        assert puppetfile.forge_modules == []
        puppetfile.add_forge_module('puppetlabs/apache', '0.1.10')
        forge_module_apache = ForgeModule('puppetlabs/apache', '0.1.10')
        assert forge_module_apache in puppetfile.forge_modules
        github_repository.update_file.assert_called_once_with(
            "/Puppetfile",
            "Puppetfile - Add forge module puppetlabs/apache",
            "mod 'puppetlabs/apache', '0.1.10'\n",
            "shasha")

    @staticmethod
    def test_it_cannot_add_an_existing_module():
        github_repository = MagicMock()
        content = github_repository.get_file_contents()
        content.decoded_content.decode.return_value = ('')
        forge_module_apache = ForgeModule('puppetlabs/apache')
        puppetfile = Puppetfile(github_repository,
                                'env',
                                sha='shasha',
                                forge_modules=[forge_module_apache])
        with pytest.raises(ModuleAlreadyPresentException):
            puppetfile.add_forge_module('puppetlabs/apache')


class TestPuppetfileUpdateGitModule:
    @staticmethod
    def test_it_update_a_git_module_in_the_puppetfile():
        github_repository = MagicMock()
        content = github_repository.get_file_contents()
        content.decoded_content.decode.return_value = ('')
        puppetfile = Puppetfile(github_repository,
                                'env',
                                sha='shasha',
                                git_modules=[deepcopy(GIT_MODULE_APACHE)])
        assert puppetfile.git_modules[0].reference == 'ed19f'
        puppetfile.update_git_module('apache', 'a76f6fb')
        assert puppetfile.git_modules[0].reference == 'a76f6fb'
        github_repository.update_file.assert_called_once_with(
            "/Puppetfile",
            "Puppetfile - Update git module apache from ed19f to a76f6fb",
            ("mod 'apache',\n"
             "  :git => 'https://url/git/apache',\n"
             "  :ref => 'a76f6fb'\n"),
            "shasha")

    @staticmethod
    def test_it_update_a_git_module_reference_and_reference_type():
        github_repository = MagicMock()
        content = github_repository.get_file_contents()
        content.decoded_content.decode.return_value = ('')
        puppetfile = Puppetfile(github_repository,
                                'env',
                                sha='shasha',
                                git_modules=[deepcopy(GIT_MODULE_APACHE)])
        assert puppetfile.git_modules[0].reference == 'ed19f'
        puppetfile.update_git_module('apache',
                                     'master',
                                     reference_type='branch')
        assert puppetfile.git_modules[0].reference == 'master'
        assert puppetfile.git_modules[0].reference_type == 'branch'

    @staticmethod
    def test_it_cannot_update_a_missing_git_module():
        github_repository = MagicMock()
        content = github_repository.get_file_contents()
        content.decoded_content.decode.return_value = ('')
        puppetfile = Puppetfile(github_repository, 'env', sha='shasha')
        assert puppetfile.git_modules == []
        with pytest.raises(ModuleNotFoundException):
            puppetfile.update_git_module('apache', 'updatebranch')


class TestPuppetfileUpdateForgeModule:
    @staticmethod
    def test_it_update_a_module_in_the_puppetfile():
        github_repository = MagicMock()
        content = github_repository.get_file_contents()
        content.decoded_content.decode.return_value = ('')
        forge_module_apache = ForgeModule('puppetlabs/apache', '0.1.1')
        puppetfile = Puppetfile(github_repository,
                                'env',
                                sha='shasha',
                                forge_modules=[forge_module_apache])
        assert puppetfile.forge_modules[0].version == '0.1.1'
        puppetfile.update_forge_module('puppetlabs/apache', version='0.1.2')
        assert puppetfile.forge_modules[0].version == '0.1.2'
        github_repository.update_file.assert_called_once_with(
            "/Puppetfile",
            ("Puppetfile - Update forge module puppetlabs/apache "
             "from 0.1.1 to 0.1.2"),
            "mod 'puppetlabs/apache', '0.1.2'\n",
            "shasha")

    @staticmethod
    def test_it_cannot_update_a_missing_module():
        github_repository = MagicMock()
        content = github_repository.get_file_contents()
        content.decoded_content.decode.return_value = ('')
        puppetfile = Puppetfile(github_repository, 'env', sha='shasha')
        assert puppetfile.forge_modules == []
        with pytest.raises(ModuleNotFoundException):
            puppetfile.update_forge_module('puppetlabs/apache', '0.1.2')


class TestPuppetfileListModules:
    @staticmethod
    def test_it_returns_the_list_of_modules():
        github_repository = MagicMock()
        content = github_repository.get_file_contents()
        content.decoded_content.decode.return_value = ('')
        git_module_custommod = GitModule('custommod',
                                         'https://url/git/custommod')
        forge_module_apache = ForgeModule('puppetlabs/apache', '0.1.10')
        forge_module_vcsrepo = ForgeModule('puppetlabs/vcsrepo', '0.2.10')
        puppetfile = Puppetfile(github_repository,
                                'env',
                                sha='shasha',
                                forge_modules=[forge_module_apache,
                                               forge_module_vcsrepo],
                                git_modules=[git_module_custommod])
        assert sorted(puppetfile.list_modules()) == sorted(['custommod',
                                                            'puppetlabs/apache',
                                                            'puppetlabs/vcsrepo'])
