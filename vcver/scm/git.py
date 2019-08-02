import os
import logging
import subprocess
from .base import SCM, extract_tag_version, DEFAULT_TAG_VERSION
from ..exception import VersionerError

CMD_LATEST_VERSION_TAG = "git describe --tags --match 'v*' --abbrev=0"
CMD_BRANCH = "git rev-parse --abbrev-ref HEAD"
CMD_SHOW_BRANCHES = "git branch --points-at=HEAD"
CMD_REV_LIST = "git rev-list HEAD --reverse"
CMD_LIST_TAGS = "git tag --list"
CMD_REV_COUNT = "git rev-list {start}..{end} --count"
CMD_SHORT_HASH = "git rev-parse --short HEAD"

LOG = logging.getLogger(__name__)


class GitCommandError(VersionerError):
    pass


class Git(SCM):

    RELEASE_BRANCH_REGEX = "master"

    @staticmethod
    def is_repo(path):
        """
        Detects if path is inside a valid Git repo.

        Parameters:
        path: Path

        Returns:
        True, path is in Git repo. False, path is not in Git repo.
        """
        head, tail = os.path.split(os.path.abspath(path))
        while tail:
            dot_git_path = os.path.join(head, tail, ".git")
            if os.path.exists(dot_git_path):
                return True
            path = head
            head, tail = os.path.split(path)
        return False

    def get_properties(self):
        tag, tag_version = self.get_latest_version_tag()
        return {
            "scm_change_id": "x" + self._cmd(CMD_SHORT_HASH),
            "commit_count": self._num_commits_since(tag),
            "tag_version": tag_version,
            "branch": self._branch(),
        }

    def _branch(self):
        branch_line = self._cmd(CMD_SHOW_BRANCHES).split("\n")
        branch_candidate = None
        for line in branch_line:
            # strip leading *
            line = line[len("* ") :]
            if "detached" in line:
                continue
            return line

        if branch_candidate is None and "GIT_BRANCH" in os.environ:
            return os.environ["GIT_BRANCH"]

        return branch_candidate

    def _num_commits_since(self, tag):
        cmd = CMD_REV_COUNT.format(start=tag, end="HEAD")
        return self._cmd(cmd)

    def _get_first_commit(self):
        all_revisions = self._cmd(CMD_REV_LIST)
        return all_revisions.partition("\n")[0]

    def get_latest_version_tag(self):
        try:
            tag = self._cmd(CMD_LATEST_VERSION_TAG)
            commit = tag
        except GitCommandError:
            LOG.info("unable to find a valid version tag. using the default.")
            tag = "v" + DEFAULT_TAG_VERSION
            commit = self._get_first_commit()
        extracted_version = extract_tag_version(tag)
        return (commit, extracted_version)

    def _cmd(self, cmd):
        """
        Arguments:
            cmd - command to run

        Returns the output of the command.
        """
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=self._path,
        )
        stdout, stderr = proc.communicate()
        stdout = stdout.decode("utf-8").strip()
        stderr = stderr.decode("utf-8").strip()
        LOG.debug("stdout of cmd: " + stdout)
        LOG.debug("stderr of cmd: " + stderr)

        if proc.returncode == 0:
            return stdout
        raise GitCommandError(
            "'{0}' returned an error code {1}".format(cmd, proc.returncode)
        )
