#!/usr/bin/env bash
# Creates tools/.venv and installs dependencies.
# Run once after copying this template to a new wiki instance.
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Creating virtual environment at tools/.venv ..."
python3 -m venv .venv

echo "Installing dependencies ..."
.venv/bin/pip install --upgrade pip -q
.venv/bin/pip install -r requirements.txt -q

echo ""
echo "Setup complete."
echo "Tools will use: $SCRIPT_DIR/.venv/bin/python"
echo ""
echo "Test:"
echo "  tools/.venv/bin/python tools/search.py --help"
echo "  tools/.venv/bin/python tools/fetch_link.py https://example.com"
