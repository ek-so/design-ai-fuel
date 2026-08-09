#!/usr/bin/env bash
# Ensures .claude, .cursor, and CLAUDE.md are filesystem symlinks.
# Git may check these out as plain text files when core.symlinks is false.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -d .agents ]]; then
  echo "setup-symlinks: .agents not found — are you in the repo root?" >&2
  exit 1
fi

link_ok() {
  local path="$1" target="$2"
  [[ -L "$path" ]] && [[ "$(readlink "$path")" == "$target" ]]
}

fix_link() {
  local path="$1" target="$2"

  if link_ok "$path" "$target"; then
    return 1
  fi

  if [[ -e "$path" ]] || [[ -L "$path" ]]; then
    rm -rf "$path"
  fi

  ln -sf "$target" "$path"
  return 0
}

fixed=0

if fix_link .claude .agents; then
  echo "setup-symlinks: linked .claude -> .agents"
  fixed=1
fi

if fix_link .cursor .agents; then
  echo "setup-symlinks: linked .cursor -> .agents"
  fixed=1
fi

if fix_link CLAUDE.md AGENTS.md; then
  echo "setup-symlinks: linked CLAUDE.md -> AGENTS.md"
  fixed=1
fi

exit 0
