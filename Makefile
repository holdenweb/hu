POETRY=poetry

test:
	$(POETRY) run pytest -v

full_test:
	$(POETRY) run tox

local_ci:
	circleci local execute

build:
	python version.py
