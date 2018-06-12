import pytest

from ppfilemgr.exceptions import ModuleBadGitReferenceTypeExcption
from ppfilemgr.puppet_module import GitModule


class TestGitModule:
    def test_it_raise_bad_git_reference_type_with_unknow_reference(self):
        with pytest.raises(ModuleBadGitReferenceTypeExcption):
            GitModule('nginx', 'https://url/repo/nginx.git', 'bad_ref',
                      'version')
