from unittest.mock import MagicMock, patch

from github import GithubException
import pytest

from control_repository.control_repository import ControlRepository
from control_repository.exceptions import (ControlRepositoryException,
                                           EnvironmentNotFoundException)
from control_repository.puppet.environment import Environment


class TestControlRepository:
    @staticmethod
    @patch('control_repository.control_repository.Github')
    def test_it_get_control_repository_from_github(github):
        ControlRepository('organization',
                          'repository',
                          'some-token')
        github.assert_called_once()
        github.assert_called_once_with('some-token')
        github().get_organization.assert_called_once_with('organization')
        github().get_organization().get_repo.assert_called_once_with('repository')

    @staticmethod
    @patch('control_repository.control_repository.Github')
    def test_it_fails_to_get_control_repository_from_github(github):
        github.side_effect = GithubException('badstatus', 'missing')
        with pytest.raises(ControlRepositoryException):
            ControlRepository('test_organization',
                              'test_repository',
                              'some-token')


class TestControlRepositoryGetEnvironment:
    @staticmethod
    @patch('control_repository.control_repository.Github', MagicMock())
    def test_it_returns_a_puppet_environment():
        control_repository = ControlRepository('test_organization',
                                               'test_repository',
                                               'some-token')
        puppet_environment = control_repository.get_environment('test')
        assert isinstance(puppet_environment, Environment)

    @staticmethod
    @patch('control_repository.control_repository.Github')
    def test_if_environment_does_not_exists(github):
        control_repository = ControlRepository('test_organization',
                                               'test_repository',
                                               'some-token')
        repository = github().get_organization().get_repo()
        repository.get_branch.side_effect = GithubException('badstatus', 'missing')
        with pytest.raises(EnvironmentNotFoundException):
            control_repository.get_environment('environment')


class TestControlRepositoryGetEnvironmentNames:
    @staticmethod
    @patch('control_repository.control_repository.Github')
    def test_it_returns_the_list_of_environment_names(github):
        control_repository = ControlRepository('test_organization',
                                               'test_repository',
                                               'some-token')
        repository = github().get_organization().get_repo()
        branch_dev = MagicMock()
        branch_prd = MagicMock()
        branch_dev.configure_mock(name='dev')
        branch_prd.configure_mock(name='prd')
        repository.get_branches.return_value = [branch_dev, branch_prd]
        environment_list = control_repository.get_environment_names()
        assert sorted(environment_list) == sorted(['prd', 'dev'])


class TestControlRepositoryGetEnvironments:
    @staticmethod
    @patch('control_repository.control_repository.Github')
    def test_it_returns_all_puppet_environments(github):
        control_repository = ControlRepository('test_organization',
                                               'test_repository',
                                               'some-token')
        repository = github().get_organization().get_repo()
        branch_dev = MagicMock()
        branch_prd = MagicMock()
        branch_dev.configure_mock(name='dev')
        branch_prd.configure_mock(name='prd')
        repository.get_branches.return_value = [branch_dev, branch_prd]
        puppet_environments = control_repository.get_environments()
        assert isinstance(puppet_environments[0], Environment)
        assert puppet_environments[0].name == 'dev'
        assert isinstance(puppet_environments[1], Environment)
        assert puppet_environments[1].name == 'prd'
