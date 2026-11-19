#!/usr/bin/env bash
# One-time setup for macOS and Linux.
# Installs uv (if missing), Python 3.14, and all project dependencies.
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v uv >/dev/null 2>&1; then
  echo "==> Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

echo "==> Installing Python and dependencies..."
uv sync

echo
echo "Setup complete. Start the app with:"
echo "  ./scripts/run.sh"
echo "(If 'uv' is not found in a new terminal, close and reopen the terminal.)"
