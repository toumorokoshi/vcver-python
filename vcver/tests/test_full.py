import vcver


def test_happy_case():
    """
    instead of setting up a git repo,
    just testing that vcver's own
    version string matches the
    expected format.
    """
    v = vcver.get_version()
    version, scm = v.split("+")
    major, minor, patch, dev = version.split(".")
    branch, change_id = scm.split(".")
    assert change_id.startswith("x")
    change_id = change_id[1:]
    # scm_change_id should be a git hash
    assert set(change_id) & set("abcdef1234567890") == set(change_id)
    # major / minor should be an int
    int(major)
    int(minor)
    int(patch)
    assert dev.startswith("dev")
    # commitcount should be an int
    int(dev[3:])
