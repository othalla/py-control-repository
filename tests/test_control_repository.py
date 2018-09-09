from unittest.mock import MagicMock, patch

from github import GithubException
from github import Repository
import pytest

from control_repository.control_repository import ControlRepository
from control_repository.puppet import Environment


class TestControlRepository:
    @staticmethod
    @patch('control_repository.control_repository.Github')
    def test_it_get_control_repository_from_github(mock_github):
        ControlRepository('test_organization',
                          'test_repository',
                          'some-token')
        mock_github.assert_called_once()
        mock_github.assert_called_once_with('some-token')


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
    @patch('control_repository.control_repository.Github', MagicMock())
    def test_if_environment_does_not_exists():
        control_repository = ControlRepository('test_organization',
                                               'test_repository',
                                               'some-token')
        with pytest.raises(GithubException):
            control_repository.get_environment('missing_environment')
