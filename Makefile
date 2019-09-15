POETRY=poetry

test:
	$(POETRY) run pytest -v

full_test:
	$(POETRY) run tox
