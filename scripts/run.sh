#!/usr/bin/env bash
# Start the app on macOS and Linux. Opens at http://localhost:8501
set -euo pipefail

cd "$(dirname "$0")/.."
export PATH="$HOME/.local/bin:$PATH"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv is not installed. Run ./scripts/setup.sh first."
  exit 1
fi

uv run streamlit run streamlit_app.py "$@"
