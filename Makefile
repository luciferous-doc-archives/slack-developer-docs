SHELL = /usr/bin/env bash -xeuo pipefail

format:
	uv run isort src/
	uv run black src/

renovate:
	renovate --platform=local

.PHONY: \
	format \
	renovate

