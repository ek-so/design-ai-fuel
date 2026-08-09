#!/usr/bin/env bash
# Activate the design-ai-fuel Google Workspace venv.
# Usage: source .agents/_utils/google/activate.sh

HOME_DIR="${DESIGN_AI_FUEL_HOME:-$HOME/.design-ai-fuel}"
VENV_DIR="$HOME_DIR/.venv"

if [[ ! -f "$VENV_DIR/bin/activate" ]]; then
  echo "Venv not found at $VENV_DIR" >&2
  echo "Run: .agents/_utils/google/setup.sh" >&2
  return 1 2>/dev/null || exit 1
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
echo "Activated: $VENV_DIR"
