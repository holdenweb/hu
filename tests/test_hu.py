from hu import __version__
from hu import ObjectDict


def test_old_import():
    "Verify that a backwards-compatible import still works."
    from hu.object_dict import ObjectDict as OD

    assert OD is ObjectDict
