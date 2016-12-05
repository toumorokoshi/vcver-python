def make_string_pep440_compatible(raw_str):
    """
    pep440 only allows a subset of characters in the
    version name:

    - alphanumeric
    - dots

    this will restrict the string to that set.
    """
