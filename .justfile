export PYTHONPATH := "src"

clean:
    find src tests -name __pycache__ -exec rm -r {} \; -prune

dist-test:
    #!/usr/bin/env bash
    PROJECT_DIR=`pwd`
    DIR=`mktemp -d`
    cd ${DIR}
    git clone ${PROJECT_DIR}
    cd `basename ${PROJECT_DIR}`
    (uv venv --python 3.13 && uv run just test)
    rm -rf ${DIR}

test:
    uv run pytest -v

tox-test:
    tox -q

build:
    python build_hu.py

style-check:
    poetry run flake8 src && echo flake8 done

watch-test:
    @make test --silent || exit 0
    @poetry run watchmedo shell-command --patterns="*.py" --recursive --drop --command="make test --silent" .
