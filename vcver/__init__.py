import os
import logging
from .scm.git import Git
from .exception import VersionerError
from .dist import extract_release_argv

SCM_TYPES = [Git]
LOG = logging.getLogger(__name__)
RELEASE_FORMAT = "{tag_version}"
FORMAT = "{tag_version}.dev{commit_count}+{branch}.{scm_change_id}"


def setup_keywords_entry_point(dist, attr, value):
    logging.basicConfig()
    version = get_version(value)
    dist.metadata.version = version


def get_version(path=os.curdir,
                extract_release_arg=False,
                branch_config=None,
                version_format=FORMAT,
                release_version_format=RELEASE_FORMAT,
                version_file="VERSION",
                scm_type=None):
    """
    return the version.
    """
    is_release = False
    if extract_release_arg:
        is_release = extract_release_argv()

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

    fmt_to_use = release_version_format if is_release else version_format

    try:
        version = fmt_to_use.format(**props)
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
