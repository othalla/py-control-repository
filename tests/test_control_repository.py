from unittest.mock import Mock

from github import GithubException
import pytest

from control_repository.control_repository import ControlRepository


class TestControlRepositoryGetEnvironment:
    @staticmethod
    def test_it_returns_a_puppet_environment():
        control_repository = ControlRepository('test_organization',
                                               'test_repository',
                                               'some-token')
