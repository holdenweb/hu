from hw import __version__, ObjectDict
import toml


def test_version():
    "Ensure that hw reports the version set in pyproject.toml."
    # Should this test only be a pre-merge hook or similar?
    with open("pyproject.toml") as f:
        # ``we now eat our own dogfood for the first time
        pyproj = ObjectDict(toml.load(f))
    assert __version__ == pyproj.tool.poetry.version


def test_old_import():
    "Verify that a backwards-compatible import still works."
    from hw.object_dict import ObjectDict as OD

    assert OD is ObjectDict
