#!/usr/bin/env bash
# Create ~/.design-ai-fuel/.venv and install Google API dependencies.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOME_DIR="${DESIGN_AI_FUEL_HOME:-$HOME/.design-ai-fuel}"
VENV_DIR="$HOME_DIR/.venv"
REQS="$SCRIPT_DIR/requirements.txt"

mkdir -p "$HOME_DIR/output"

if [[ ! -d "$VENV_DIR" ]]; then
  python3 -m venv "$VENV_DIR"
  echo "Created venv: $VENV_DIR"
else
  echo "Using existing venv: $VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
pip install --upgrade pip >/dev/null
pip install -r "$REQS"

echo
echo "Setup complete."
echo "1. Place your OAuth Desktop client at:"
echo "   $HOME_DIR/client_secret.json"
echo "2. Activate the venv:"
echo "   source $SCRIPT_DIR/activate.sh"
echo "3. Run any CLI (browser opens once for consent)."
echo "See $SCRIPT_DIR/README.md for GCP console steps."
