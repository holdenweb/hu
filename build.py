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
# Get version to be released from poetry and parse
#
p_version = run_cmd(["poetry", "version"]).decode("ascii")
name, release_version = p_version.strip().split()
rv = semver.VersionInfo.parse(release_version)
if rv.prerelease:
    stage = tuple(rv.prerelease.split("."))
else:
    stage = None
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

with open(f"src/{name}/_version.py", "w") as v_file:
    v_file.write(
        f"""\
#
# Created automatically when registering a new version
# Edits made here will be lost when build.py is re-run.
#
__version__ = "{rv}"
"""
    )
run_cmd(f"git add src/{name}/_version.py".split())
run_cmd("poetry build".split())
run_cmd(["git", "commit", "-m", f"Auto-build of {release_tag}"])
run_cmd(["git", "tag", release_tag])
