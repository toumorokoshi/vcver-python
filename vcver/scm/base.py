class SCM(object):
    """
    SCMs are wrappers around a particular form of version control.
    """
    REQUIRED_PARAMS = [
        "tag_version",
        "commitcount",
        "scm_change_id"
    ]

    def __init__(self, path):
        self._path = path

    @staticmethod
    def is_repo(path):
        """
        should return True if it is a valid
        repo of the provided scm type.
        """
        return False

    def get_properties(self):
        """
        return back a dictionary containing
        all properties exposed by this scm.
        """
        return {}


def extract_tag_version(tag):
    """
    extract a version string from a tag, or None if
    it is not a valid numerical version.
    """
