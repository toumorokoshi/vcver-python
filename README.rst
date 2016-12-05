============
vcver Python
============

--------------
What is vcver?
--------------

vcver is an approach for versioning that heavily relies on the version control
system of choice for determining version strings.

There are two categories of version strings:

develop versions, of the form:

.. code-block::

    {tag_version}.dev{commit_count}+{branch}.{scm_change_id}

and a release version, of the form:

.. code-block::

    {tag_version}

Each part is described as follows:

* tag_version is retrieved from the last tagged commit with a leading v (e.g. v1.0)
* commitcount is the number of commits from tag_version
* branch is the branch that the repository was built against, removing
  characters that are incompatible with PEP440 (anything that is not alphanumeric or a dot)
* scm_change_id is a unique id in the form of version control, used to identify
  the change that was used to build this version.

For example, in a git repository, on a master branch with the most recent tag of
v1.1, the dev version would look something like:

.. code-block::

   1.1.dev10+master.abc123

And a release version:

.. code-block::

   1.1

These are version string styles that are compatible with
`PEP440`<https://www.python.org/dev/peps/pep-0440/>.


-------
Example
-------

Add a MANIFEST.in to your package, if you do not already have one. Then add the following:

.. code-block::

   include VERSION

It's also recommended to ignore this file in your version control.

Then, follow this pattern in your setup.py:

.. code-block:: python


    # OPTIONAL, but recommended:
    # this block is useful for specifying when a build should
    # use the 'release' version. it allows specifying a release version
    # with an additional argument in the setup.py:
    # $ python setup.py upload --release
    import sys
    is_release = False
    if "--release" in sys.argv:
        sys.argv.remove("--release")
        is_release = True

    # OPTIONAL, but recommended:
    # vcver writes a version file relative to the
    # current working directory by default.
    # It's recommended to provide it with your
    # setup.py directory instead (in case someone
    # runs your setup.py from a different directory)
    base = os.path.dirname(os.path.abspath(__file__))

    setup(name='aiohttp-transmute',
        # add the following two lines,
        # and do not specify a version.
        setup_requires=["vcver"],
        # vcver will only produce a release
        # version if "is_release" is True.
        vcver={
            "is_release": is_release,
            "path": base
        },
        ...
    )

Now your package will publish with a VC-based version!

If you followed the full example, you can specify the release version by adding --release:

    python setup.py upload --release

-------------------
FAQ / Other Details
-------------------

Why a dev and release version?
==============================

The dev and release versions have different goals:

* dev: to provide as much information as possible to quickly identify
  where the current version originated from in regard to version control.
* release: to provide a clear version that helps the consumer understand what changed.

For most consumers, the number of commits since the last release, the
branch it was released against, or the build commit itself are
irrelevant.  The consumer wants to know how much this version changed,
and that can be done by the major / minor / patch versions specified
in the git tag. Adding this information proves to be confusing with
that regard, providing multiple numbers that are not relevant to figuring out
the amount of change.

Version String Elements
=======================

The default version string for vcver is of the form::

    {tag_version}.dev{commit_count}+{branch}.{scm_change_id}

Where:



How to make sure others can consume your package
================================================

If you followed the example, you already have this.

Once vcver is called, a VERSION file is created in the current working
directory, which is typically the same directory as where the setup.py lives
(you can make it more accurate, see the example)

vcver will attempt to find a VERSION file if the working directory is
not a version control repository. Make sure your package includes a
VERSION file by creating/modifying the
`MANIFEST.in`<https://docs.python.org/2/distutils/sourcedist.html#the-manifest-in-template>:

.. code-block::

   include VERSION


Pre-PEP440 Version
==================

Some (much older) versions of setuptools are unable to consume the dev version string,
due to the plus in the version string.

If you need backwards compatibility and you would still like vc versioning, the
following format is recommended:

      {tag_version}.dev{commit_count}.{branch}.{scm_change_id}

 This can be changed by an argument into vcver:

.. code-block:: python

    # in the setup call of setup.py
    vcver={"version_format": "{tag_version}.dev{commit_count}.{branch}.{scm_change_id}"}

Compatibility with Semantic Versioning
======================================

`Semantic versioning`<http://semver.org/> is a standard to provided a
meaning to the major, minor, and patch versions of a version
string. Compatibility with semver is possible if new major / minor
versions are tagged according the semver spec.

--------------
Special Thanks
--------------

- `Zillow`<http://www.zillow.com/jobs/>, where this approach of SCM-based versioning started
- `Taylor McKay`<https://github.com/tmckay>  who implemented the original Python version at Zillow
- `Mohammad Sarhan`<https://github.com/sarhanm>, who designed and implemented the original Java version at Zillow, and has a public `gradle variant`<https://github.com/sarhanm/gradle-versioner>
