import os
from mock import Mock
from vcver.scm.git import Git


def test_git_branch_environ():
    git = Git("/tmp/")
    git._cmd = Mock(return_value="HEAD")
    os.environ["GIT_BRANCH"] = "foo"
    try:
        assert git._branch() == "foo"
    finally:
        del os.environ["GIT_BRANCH"]
