#!/usr/bin/env bash
set -euo pipefail

stop_port() {
  local port="$1"

  if command -v lsof >/dev/null 2>&1; then
    local pids
    pids="$(lsof -ti tcp:"$port" || true)"
    if [ -n "$pids" ]; then
      echo "Apagando procesos en puerto $port..."
      kill $pids 2>/dev/null || true
    fi
    return
  fi

  if command -v fuser >/dev/null 2>&1; then
    if fuser "$port/tcp" >/dev/null 2>&1; then
      echo "Apagando procesos en puerto $port..."
      fuser -k "$port/tcp" >/dev/null 2>&1 || true
    fi
  fi
}

stop_port 8000
stop_port 5173

echo "ERMA apagada."
