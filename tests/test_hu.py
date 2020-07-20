import dunamai
from hu import __version__
from hu import ObjectDict


def test_version():
    """
    Fail if the current git state is dirty.
    """
    "Ensure that hu reports the version set in pyproject.toml."
    # Should this test only be a pre-merge hook or similar?\
    version = dunamai.Version.from_git()
    assert version.distance, "This code is already tagged."
    assert not version.dirty, "This code not comitted to source control."


def test_old_import():
    "Verify that a backwards-compatible import still works."
    from hu.object_dict import ObjectDict as OD

    assert OD is ObjectDict
