clean:
    find src tests -name __pycache__ -exec rm -r {} \; -prune

# verify a git clone passes all tests
dist-test:
    #!/usr/bin/env bash
    PROJECT_DIR=`pwd`
    DIR=`mktemp -d`
    cd ${DIR}
    git clone ${PROJECT_DIR}
    cd `basename ${PROJECT_DIR}`
    uv run just test
    rm -rf ${DIR}

# test locally
test:
    uv run pytest -v

tox-test:
    uv run tox -q

build:
    uv build

style-check:
    uv run ruff check src
