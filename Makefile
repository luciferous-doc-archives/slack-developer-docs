SHELL = /usr/bin/env bash -xeuo pipefail

format:
	uv run isort src/
	uv run black src/

renovate:
	renovate --platform=local

test-unit:
	uv run pytest -vv tests/unit 

.PHONY: \
	format \
	renovate

