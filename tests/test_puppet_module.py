import pytest

from control_repository.exceptions import (ModuleBadGitReferenceTypeExcption,
                                           ModuleParserException)
from control_repository.puppet_module import GitModule, ForgeModule


class TestGitModule:
    def test_with_unknow_reference(self):
        with pytest.raises(ModuleBadGitReferenceTypeExcption):
            GitModule('nginx', 'https://url/repo/nginx.git', 'bad_reference',
                      'version')


class TestForgemodule:
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
