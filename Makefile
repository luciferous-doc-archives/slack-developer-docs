SHELL = /usr/bin/env bash -xeuo pipefail

format:
	uv run isort src/
	uv run black src/

.PHONY: \
	format

