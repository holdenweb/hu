POETRY=poetry

.PHONY: test full_test local_ci build style_check watch-test

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

watch-test:
	@make test --silent || exit 0
	@poetry run watchmedo shell-command --patterns="*.py" --recursive --drop --command="make test --silent" .
