POETRY=poetry

.PHONY: test full_test local_ci build style_check watch-test

clean:
	find src tests -name __pycache__ -exec rm -r {} \; -prune

dist-test:
	PROJECT_DIR=$$(pwd) ; \
	DIR=$$(mktemp -d) ; \
	cd $${DIR} && \
	git clone $${PROJECT_DIR} && \
	cd $$(basename $${PROJECT_DIR}) && \
	(poetry env use 3.13 && poetry install && poetry run make test) && \
	rm -rf $${DIR}
test:
	$(POETRY) run pytest -v

tox-test:
	tox -q

build:
	python build_hu.py

style-check:
	poetry run flake8 src && echo flake8 done

watch-test:
	@make test --silent || exit 0
	@poetry run watchmedo shell-command --patterns="*.py" --recursive --drop --command="make test --silent" .
