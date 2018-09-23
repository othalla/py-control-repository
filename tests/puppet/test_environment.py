from unittest.mock import MagicMock

import pytest

from control_repository.exceptions import PuppetfileNotFoundException
from control_repository.puppet.environment import Environment
from control_repository.puppet.puppetfile import Puppetfile


class TestEnvironmentGetPuppetfile:
    @staticmethod
    def test_it_returns_a_puppetfile():
        github_repository = MagicMock()
        github_repository.get_file_contents().decoded_content.return_value = ''
        environment = Environment('production', github_repository)
        puppetfile = environment.get_puppetfile()
        assert isinstance(puppetfile, Puppetfile)

    @staticmethod
    def test_if_puppetfile_missing():
        github_repository = MagicMock()
        github_repository.get_file_contents.side_effect = PuppetfileNotFoundException
        with pytest.raises(PuppetfileNotFoundException):
            environment = Environment('production', github_repository)
            environment.get_puppetfile()
