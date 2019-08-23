POETRY=$$HOME/bin/poetry

test:
	$(POETRY) run pytest -v
