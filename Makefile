SHELL := /bin/sh
PYTHON := python3
VENV := .venv
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest

.PHONY: help venv install test tree

help: ## Tampilkan daftar target
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "%-12s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

venv: ## Buat virtual environment .venv (idempotent)
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)

install: venv ## Install dependencies ke .venv
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt

test: ## Jalankan pytest
	@$(PYTEST)

tree: ## Tampilkan struktur folder
	@$(PYTHON) - <<'PY'
from pathlib import Path
root = Path('.')
ignore = {'.venv', '.git', '__pycache__'}

def walk(path: Path, prefix: str = ''):
    entries = [p for p in sorted(path.iterdir()) if p.name not in ignore]
    for i, p in enumerate(entries):
        last = i == len(entries) - 1
        connector = '\\-- ' if last else '|-- '
        print(prefix + connector + p.name)
        if p.is_dir():
            extension = '    ' if last else '|   '
            walk(p, prefix + extension)

print(root.name)
walk(root)
PY
