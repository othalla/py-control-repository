from unittest.mock import Mock

from github import GithubException
import pytest

from control_repository.control_repository import ControlRepository
from control_repository.puppet_module import ForgeModule
from control_repository.puppetfile import Puppetfile


class TestControlRepository:
    def test_parse_calls_right_functions_without_errors(self):
        file_content = Mock(name='file_content')
        file_content.return_value = ['line1', 'line2']
        parse_puppetfile = Mock(name='parse_puppetfile')
        control_repo = ControlRepository('env', 'orga', 'repo', 'token')
        control_repo.parse(file_provider=file_content, parser_provider=parse_puppetfile)
        file_content.assert_called_once_with('env', 'orga', 'repo', 'token', None, 'Puppetfile')
        parse_puppetfile.assert_called_once_with(['line1', 'line2'])

    def test_parse_raise_github_exception_if_file_content_fails(self):
        file_content = Mock(name='file_content')
        file_content.side_effect = GithubException('status', 'data')
        control_repository = ControlRepository('env', 'orga', 'repo', 'token')
        with pytest.raises(GithubException):
            control_repository.parse(file_provider=file_content)

    def test_update_raise_type_error_with_bad_input_module(self):
        control_repository = ControlRepository('env', 'orga', 'repo', 'token')
        with pytest.raises(TypeError):
            control_repository.update('badmodule')

    def test_update_add_new_module_to_puppetfile(self):
        file_content = Mock(name='file_content')
        parse_puppetfile = Mock(name='parse_puppetfile')
        update_puppetfile = Mock(name='update_puppetfile')
        parse_puppetfile.return_value = Puppetfile()
        forge_module = ForgeModule('nginx', '0.0.1')
        control_repository = ControlRepository('env', 'orga', 'repo', 'token')
        control_repository.parse(file_provider=file_content,
                                 parser_provider=parse_puppetfile)
        control_repository.update(forge_module,
                                  update_puppetfile_provider=update_puppetfile)
        assert forge_module in control_repository.modules
        assert update_puppetfile.call_count == 1

    def test_update_existing_module_does_nothing_with_same_version(self):
        forge_module = ForgeModule('nginx', '0.0.1')
        file_content = Mock(name='file_content')
        update_puppetfile = Mock(name='update_puppetfile')
        parse_puppetfile = Mock(name='parse_puppetfile')
        parse_puppetfile.return_value.modules = [forge_module]
        control_repository = ControlRepository('env', 'orga', 'repo', 'token')
        control_repository.parse(file_provider=file_content, parser_provider=parse_puppetfile)
        control_repository.update(forge_module, update_puppetfile_provider=update_puppetfile)
        assert update_puppetfile.call_count == 0

    def test_update_existing_module_does_change_puppetfile(self):
        file_content = Mock(name='file_content')
        update_puppetfile = Mock(name='update_puppetfile')
        parse_puppetfile = Mock(name='parse_puppetfile')
        ppfile = Puppetfile()
        ppfile.add_module(ForgeModule('nginx', '0.0.1'))
        parse_puppetfile.return_value = ppfile
        control_repo = ControlRepository('env', 'orga', 'repo', 'token')
        control_repo.parse(file_provider=file_content, parser_provider=parse_puppetfile)
        forge_module = ForgeModule('nginx', '0.0.2')
        control_repo.update(forge_module, update_puppetfile_provider=update_puppetfile)
        assert forge_module == control_repo.modules[0]
        assert update_puppetfile.call_count == 1
