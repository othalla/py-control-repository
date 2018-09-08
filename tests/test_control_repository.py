from unittest.mock import Mock

from github import GithubException
import pytest

from control_repository.control_repository import ControlRepository
from control_repository.puppet import Environment


class TestControlRepositoryGetEnvironment:
    @staticmethod
    def test_it_returns_a_puppet_environment():
        control_repository = ControlRepository('test_organization',
                                               'test_repository',
                                               'some-token')
        puppet_environment = control_repository.get_environment('test')
        assert isinstance(puppet_environment, Environment)

    @staticmethod
    def test_if_environment_does_not_exists():
        control_repository = ControlRepository('test_organization',
                                               'test_repository',
                                               'some-token')
        with pytest.raises(GithubException):
            control_repository.get_environment('missing_environment')
