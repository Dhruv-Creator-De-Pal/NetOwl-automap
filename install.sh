#!/usr/bin/env bash
set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "Error: run installer with sudo."
  echo "Usage: sudo ./install.sh"
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 is required."
  exit 1
fi

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${PROJECT_DIR}"

echo "Installing AutoMap from: ${PROJECT_DIR}"

if python3 -m pip install -e .; then
  :
else
  echo "Normal pip install failed. Retrying with --break-system-packages..."
  python3 -m pip install --break-system-packages -e .
fi

echo
echo "AutoMap installed."
echo
echo "Run a scan with Ollama:"
echo "  sudo automap scan 192.168.1.0/24 --mode quick --ai-host http://localhost:11434 --ai-model llama3"
echo
echo "You can also pass a full Ollama chat endpoint:"
echo "  sudo automap scan 192.168.1.0/24 --mode quick --ai-host http://localhost:11434/api/chat --ai-model llama3"
