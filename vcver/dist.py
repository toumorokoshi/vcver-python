import sys


def extract_release_argv():
    if "--vcver-release" in sys.argv:
        sys.argv.remove("--vcver-release")
        return True
    return False
