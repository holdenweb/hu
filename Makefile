POETRY=poetry

test:
	$(POETRY) run pytest -v

full_test:
	$(POETRY) run tox

local_ci:
	circleci local execute

build:
	python build.py

style_check:
	poetry run flake8 src && echo flake8 done
	poetry run pycodestyle src && echo pycodestyle done
