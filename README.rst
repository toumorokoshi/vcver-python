============
vcver Python
============

--------------
What is vcver?
--------------

vcver is a versioning tool that includes tooling for creating versions
that allow easy correlation to the change in version control.

Defaults are also provided for a version string that is compatible
with semantic versioning, with
`PEP440`<https://www.python.org/dev/peps/pep-0440/> compatible and
incompatible variants.

----------------------
Version String Formats
----------------------

The default version string for vcver is of the form::

      {tag_version}.{commit_count}+{scm_change_id}

Where:

* tag_version is retrieved from the last tagged commit with a leading v and is numerics and dots (e.g. v1.0)
* commitcount is the number of commits from the version tag consumed
* scm_change_id is a unique id in the form of version control, used to identify
  the change that was used to build this version.

Pre-PEP440 Version
==================

Some (much older) versions of setuptools are unable to consume the default version string,
due to the plus in the version string.

If you need backwards compatibility and you would still like vc versioning, the
following format is recommended:

      {tag_version}.{commit_count}.{scm_change_id}

--------------------------------------
Compatibility with Semantic Versioning
--------------------------------------

Semantic versioning is a standard to provided a meaning to the major, minor, and patch
versions of a version string. Compatibility with semver is possible if
new major / minor versions are tagged according the semver spec.

--------------
Special Thanks
--------------

- Zillow, from where this library is inspired.
- Taylor McKay (@tmckay), who implemented the original Python version at Zillow
- Mohammad Sarhan (@sarhanm), who designed and implemented the original Java version at Zillow.
