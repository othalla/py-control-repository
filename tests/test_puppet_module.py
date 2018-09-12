import pytest

from control_repository.exceptions import (ModuleBadGitReferenceTypeExcption,
                                           ModuleParserException)
from control_repository.puppet_module import GitModule, ForgeModule


class TestGitModule:
    @staticmethod
    def test_with_unknow_reference():
        with pytest.raises(ModuleBadGitReferenceTypeExcption):
            GitModule('nginx', 'https://url/repo/nginx.git', 'bad_reference',
                      'version')


class TestGitModuleFromLines:
    @staticmethod
    def test_it_returns_git_module_without_any_reference_type():
        git_module = GitModule.from_lines(
            ["mod 'apache',",
             "    :git => 'https://github.com/puppet/apache'",
             ])
        assert git_module.name == 'apache'
        assert git_module.git_url == 'https://github.com/puppet/apache'
        assert git_module.git_reference_type == ''
        assert git_module.git_reference == ''

    @staticmethod
    def test_with_ref_reference_type_returns_git_module():
        git_module = GitModule.from_lines(
            ["mod 'apache',",
             "    :git => 'https://github.com/puppet/apache'",
             "    :ref => '0adqs1'",
             ])
        assert git_module.name == 'apache'
        assert git_module.git_url == 'https://github.com/puppet/apache'
        assert git_module.git_reference_type == 'ref'
        assert git_module.git_reference == '0adqs1'

    @staticmethod
    def test_with_branch_reference_type_returns_git_module():
        git_module = GitModule.from_lines(
            ["mod 'apache',",
             "    :git    => 'https://github.com/puppet/apache'",
             "    :branch => 'branchname'",
             ])
        assert git_module.name == 'apache'
        assert git_module.git_url == 'https://github.com/puppet/apache'
        assert git_module.git_reference_type == 'branch'
        assert git_module.git_reference == 'branchname'

    @staticmethod
    def test_with_tag_reference_type_returns_git_module():
        git_module = GitModule.from_lines(
            ["mod 'apache',",
             "    :git => 'https://github.com/puppet/apache'",
             "    :tag => '0.1.1'",
             ])
        assert git_module.name == 'apache'
        assert git_module.git_url == 'https://github.com/puppet/apache'
        assert git_module.git_reference_type == 'tag'
        assert git_module.git_reference == '0.1.1'

    @staticmethod
    def test_with_commit_reference_type_returns_git_module():
        git_module = GitModule.from_lines(
            ["mod 'apache',",
             "    :git    => 'https://github.com/puppet/apache'",
             "    :commit => '0dfa12'",
             ])
        assert git_module.name == 'apache'
        assert git_module.git_url == 'https://github.com/puppet/apache'
        assert git_module.git_reference_type == 'commit'
        assert git_module.git_reference == '0dfa12'

    @staticmethod
    def test_with_missing_git_url():
        with pytest.raises(ModuleParserException):
            GitModule.from_lines(
                ["mod 'apache',",
                 "    :commit => '0dfa12'",
                 ])


class TestForgeModuleFromLine:
    @staticmethod
    def test_it_returns_forge_module_from_line_without_version():
        forge_module = ForgeModule.from_line("mod 'puppetlabs/apache'")
        assert forge_module.name == 'puppetlabs/apache'
        assert forge_module.version == ''

    @staticmethod
    def test_it_returns_forge_module_from_line_with_version():
        forge_module = ForgeModule.from_line("mod 'puppetlabs/apache', '0.1.1'")
        assert forge_module.name == 'puppetlabs/apache'
        assert forge_module.version == '0.1.1'

    @staticmethod
    def test_it_returns_forge_module_from_line_with_version_latest():
        forge_module = ForgeModule.from_line("mod 'puppetlabs/apache', :latest")
        assert forge_module.name == 'puppetlabs/apache'
        assert forge_module.version == ':latest'

    @staticmethod
    def test_with_a_bad_module():
        with pytest.raises(ModuleParserException):
            ForgeModule.from_line("mod 'puppetlabs/apache', '0.1', 'bad'")
