import subprocess
from .base import SCM


class Git(SCM):

    @property
    def major(self):
        pass

    def _get_latest_version_tag(self):
        pass
