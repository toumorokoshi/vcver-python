import os
import logging
from .scm.git import Git
from .exception import VersionerError

SCM_TYPES = [Git]
LOG = logging.getLogger(__name__)


def main(*args, **kwargs):
    logging.basicConfig()
    return get_version(*args, **kwargs)


def get_version(path=os.curdir,
                version_format="{tag_version}.{commitcount}+{scm_change_id}",
                version_file="generated_version.txt",
                scm_type=None):
    """
    return the version.
    """
    path = os.path.abspath(path)
    version_file_path = os.path.join(path, version_file)

    scm = _get_scm(scm_type, path)
    if not scm:
        existing_version = _read_version_file(version_file_path)
        if existing_version:
            return existing_version

        if scm_type is None:
            msg = "unable to detect scm type."
        else:
            msg = "scm type {0} not found, or is not a valid repo.".format(
                scm_type
            )
        raise VersionerError(msg)

    props = scm.get_properties()
    version = version_format.format(**props)
    _write_version_file(version_file_path, version)
    return version


def _read_version_file(version_file):
    if not os.path.exists(version_file):
        return
    with open(version_file) as fh:
        return fh.read()


def _get_scm(scm_type, path):
    for SCMType in SCM_TYPES:
        if scm_type is None or scm_type == SCMType.__name__.lower():
            if scm_type.is_repo(path):
                return SCMType(path)
    return None


def _write_version_file(version_file, version):
    with open(version_file, "w+") as fh:
        fh.write(version)
