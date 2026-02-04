#!/usr/bin/env sh
set -eu

VENV=.venv
PYTHON=python3

if [ ! -d "$VENV" ]; then
  "$PYTHON" -m venv "$VENV"
fi

"$VENV/bin/pip" install --upgrade pip
"$VENV/bin/pip" install -r requirements.txt

cat <<'MSG'
NEXT STEPS
- source .venv/bin/activate
- make tree
- make test
MSG
