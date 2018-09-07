from github import Github


class ControlRepository:
    def __init__(self, github_orga: str, github_repo: str,
                 github_token: str, github_baseurl=None,
                 puppetfile_name='Puppetfile') -> None:
        self._github_orga = github_orga
        self._github_repo = github_repo
        self._github_token = github_token
        self._github_baseurl = github_baseurl

/bin/bash: :w: command not found

    def get_environment(self):
        pass
