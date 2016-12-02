import vcver


def test_happy_case():
    """
    instead of setting up a git repo,
    just testing that vcver's own
    version string matches the
    expected format.
    """
    v = vcver.get_version()
    version, scm_id = v.split("+")
    version_parts = version.split(".")
    # scm_change_id should be a git hash.
    assert set(scm_id) & set("abcdef1234567890") == set(scm_id)
    # major / minor should be an int
    int(version_parts[0])
    int(version_parts[1])
    # commitcount should be an int
    int(version_parts[2])
