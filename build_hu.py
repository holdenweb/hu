""

import subprocess
import sys

import semver


def run_cmd(arg_list):
    process = subprocess.run(arg_list, stdout=subprocess.PIPE)
    if process.stderr or process.returncode:
        msg = process.stderr if process.stderr else process.stdout
        raise ValueError(
            'Could not run command "{}\nmessage: {}"'.format(" ".join(arg_list), msg)
        )
    return process.stdout


#
# Get version to be released (hand-edited in pyproject.toml) and parse it
#
release_version = run_cmd(["uv", "version", "--short"]).decode("ascii").strip()
rv = semver.VersionInfo.parse(release_version)
release_tag = f"v{rv}"

#
# Get tag-based version from git
#
g_version = (
    run_cmd("git describe --tags --dirty --always --long".split())
    .decode("ascii")
    .strip()
)
dirty = g_version.endswith("-dirty")
if dirty:
    sys.exit("Cannot build: please commit all changes before building.")
tag, commits, ghex = g_version.rsplit("-", 2)
gv = semver.VersionInfo.parse(tag[1:])

if gv >= rv:
    sys.exit("Release version {} does not move forward from {}".format(rv, gv))

#
# The version lives only in pyproject.toml and is exposed at runtime via
# importlib.metadata (see src/hu/__init__.py), so there is no generated
# file to write or commit here -- just build the distributions and tag the
# already-committed version bump.
#
run_cmd("uv build".split())
run_cmd(["git", "tag", release_tag])
