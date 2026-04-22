SHELL = /usr/bin/env bash -xeuo pipefail

format:
	uv run isort main.py
	uv run black main.py

.PHONY: \
	format

