import sys
import pytest
from vcver.scm.git import Git


@pytest.mark.linux
@pytest.mark.parametrize(
    "inp, out",
    [
        ("/a/b", False),
        ("/a", False),
        ("/a/b/..", False),
        ("/x/", False),
        ("/..", False),
    ],
)
@pytest.mark.usefixtures("no_fs")
def test_linux_is_repo(inp, out):
    """Fails when non-repo case is not detected for linux."""
    assert Git.is_repo(inp) == out


@pytest.mark.win32
@pytest.mark.parametrize(
    "inp, out",
    [
        ("c:\\a\\b", False),
        ("c:\\a", False),
        ("c:\\x\\..", False),
        ("c:\\f\\", False),
        ("c:\\..", False),
    ],
)
@pytest.mark.usefixtures("no_fs")
def test_win32_is_repo(inp, out):
    """Fails when non-repo case is not detected for win32."""
    assert Git.is_repo(inp) == out


def test_branch_envvar(monkeypatch):
    """GIT_BRANCH should set the branch as consumed by vcver. """
    monkeypatch.setenv("GIT_BRANCH", "master")
    assert Git("")._branch() == "master"


def test_branch_strips_refs(monkeypatch):
    """
    If a ref has multiple levels (including a slash),
    remove the levels and given the final element as the branch.
    """
    monkeypatch.setenv("GIT_BRANCH", "origin/master")
    assert Git("")._branch() == "master"
