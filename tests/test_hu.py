from hu import ObjectDict

with open("version.txt", "a") as outfile:
    print(sys.version, file=outfile)


def test_old_import():
    "Verify that a backwards-compatible import still works."
    from hu.object_dict import ObjectDict as OD

    assert OD is ObjectDict
