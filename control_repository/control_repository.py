from github import Github

from control_repository.puppet_module import PuppetModule
from control_repository.parser import parse_puppetfile
from control_repository.github import update_puppetfile, get_puppetfile


class ControlRepository:
    def __init__(self, environment: str, github_orga: str, github_repo: str,
                 github_token: str, github_baseurl=None,
                 puppetfile_name='Puppetfile') -> None:
        self._environment = environment
        self._github_orga = github_orga
        self._github_repo = github_repo
        self._github_token = github_token
        self._github_baseurl = github_baseurl
        self._puppetfile_name = puppetfile_name
        self._puppetfile = None

    @property
    def modules(self):
        if self._puppetfile is not None:
            return self._puppetfile.modules
        return []

    def parse(self, file_provider=get_puppetfile,
              parser_provider=parse_puppetfile):
        if self._puppetfile is None:
            current_puppetfile = file_provider(self._environment,
                                               self._github_orga,
                                               self._github_repo,
                                               self._github_token,
                                               self._github_baseurl,
                                               self._puppetfile_name)
            self._puppetfile = parser_provider(current_puppetfile)

    def update(self, puppet_module: PuppetModule,
               update_puppetfile_provider=update_puppetfile) -> None:
        if not isinstance(puppet_module, PuppetModule):
            raise TypeError
        for module in self._puppetfile.modules:
            if module.name == puppet_module.name:
                if not module != puppet_module:  # updaten module ref changed
                    return
                self._puppetfile.update_module(puppet_module)
        self._puppetfile.add_module(puppet_module)
        return update_puppetfile_provider(self._puppetfile)
