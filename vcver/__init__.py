import os
import logging
from .scm.git import Git
from .exception import VersionerError

SCM_TYPES = [Git]
LOG = logging.getLogger(__name__)
MAIN_BRANCH_FORMAT = "{tag_version}.{commit_count}+{scm_change_id}",
DEV_BRANCH_FORMAT = "{tag_version}b{commit_count}+{branch}.{scm_change_id}",


def main(*args, **kwargs):
    logging.basicConfig()
    return get_version(*args, **kwargs)


def get_version(path=os.curdir,
                version_format=None,
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
    version_format = _get_version_format(scm, version_format)

    try:
        version = version_format.format(**props)
    except KeyError as ke:
        raise VersionerError(
            "key {0} was not provided by the scm type {1}".format(
                ke, scm.get_name())
        )

    _write_version_file(version_file_path, version)
    return version


def _read_version_file(version_file):
    if not os.path.exists(version_file):
        return
    with open(version_file) as fh:
        return fh.read()


def _get_scm(scm_type, path):
    for SCMType in SCM_TYPES:
        if scm_type is None or scm_type == SCMType.get_name():
            if SCMType.is_repo(path):
                return SCMType(path)
    return None


def _write_version_file(version_file, version):
    with open(version_file, "w+") as fh:
        fh.write(version)


def _get_version_format(scm, version_format):
    if version_format:
        return version_format

    if scm.is_main_branch():
        return MAIN_BRANCH_FORMAT

    return DEV_BRANCH_FORMAT
