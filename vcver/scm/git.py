import os
import logging
import subprocess
from .base import SCM, extract_tag_version, DEFAULT_TAG_VERSION
from ..exception import VersionerError

CMD_BRANCH = "git rev-parse --abbrev-ref HEAD"
CMD_FIRST_COMMIT = "git rev-list HEAD | tail -n 1"
CMD_LIST_TAGS = "git tag --list"
CMD_REV_COUNT = "git rev-list {start}..{end} --count"
CMD_SHORT_HASH = "git rev-parse --short HEAD"

LOG = logging.getLogger(__name__)


class Git(SCM):

    @staticmethod
    def is_repo(path):
        dot_git_path = os.path.join(path, ".git")
        return os.path.exists(dot_git_path)

    def get_properties(self):
        tag, tag_version = self.get_latest_version_tag()
        return {
            "scm_change_id": self._cmd(CMD_SHORT_HASH),
            "commit_count": self._num_commits_since(tag),
            "tag_version": tag_version,
            "branch": self._branch()
        }

    def is_main_branch(self):
        return self._branch() == "master"

    def _branch(self):
        branch = self._cmd(CMD_BRANCH)
        if branch == self._cmd(CMD_SHORT_HASH):
            # you may not be on a branch
            return None
        return branch

    def _num_commits_since(self, tag):
        cmd = CMD_REV_COUNT.format(start=tag, end="HEAD")
        return self._cmd(cmd)

    def get_latest_version_tag(self):
        tags = self._cmd(CMD_LIST_TAGS).strip().split("\n")
        for t in tags:
            if t == "":
                continue
            extracted_version = extract_tag_version(t)
            if extracted_version:
                return (t, extracted_version)
        LOG.info("unable to find a valid version tag. using the default.")
        first_commit = self._cmd(CMD_FIRST_COMMIT)
        return (first_commit, DEFAULT_TAG_VERSION)

    def _cmd(self, cmd):
        """
        Arguments:
            cmd - command to run

        Returns the output of the command.
        """
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            cwd=self._path
        )
        stdout, stderr = proc.communicate()
        LOG.debug("stdout of cmd: " + stdout)
        LOG.debug("stderr of cmd: " + stderr)

        if proc.returncode == 0:
            return stdout.decode("utf-8").strip()
        raise VersionerError(
            "'{0}' returned an error code {1}".format(
                cmd, proc.returncode
            )
        )
