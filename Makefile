.PHONY: test

lint-fix:
	uv sync
	ruff check --fix .

lint-check:
	uv sync
	ruff check .

test:
	pytest
