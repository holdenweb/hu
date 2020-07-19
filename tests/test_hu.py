import dunamai
from hu import __version__
from hu import ObjectDict


def test_version():
    "Ensure that hu reports the version set in pyproject.toml."
    # Should this test only be a pre-merge hook or similar?
    assert __version__ == str(dunamai.Version.from_git())


def test_old_import():
    "Verify that a backwards-compatible import still works."
    from hu.object_dict import ObjectDict as OD

    assert OD is ObjectDict
