from unittest.mock import MagicMock

from control_repository.puppet.environment import Environment
from control_repository.puppet.puppetfile import Puppetfile

class TestEnvironmentGetPuppetfile:
    @staticmethod
    def test_it_returns_a_puppetfile():
        github_repository = MagicMock()
        environment = Environment('production', github_repository)
        puppetfile = environment.get_puppetfile()
        assert isinstance(puppetfile, Puppetfile)
