GITHUB_TOKEN = ${GH_PAT_GETWILDS}
export GITHUB_TOKEN

lint-fix:
	uv sync
	ruff check --fix .

lint-check:
	uv sync
	ruff check .

format-fix:
	uv run ruff format .

format-check:
	uv run ruff format --check .

ipython:
	uv run --with rich --with ipython python -m IPython

py:
	uv run python

rule-main-branch:
	uv run repository.py

rule-codeowners:
	uv run codeowners.py
