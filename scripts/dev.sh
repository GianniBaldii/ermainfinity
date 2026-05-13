#!/usr/bin/env bash
set -euo pipefail

INSTALL=0
RELOAD=0
STOP_EXISTING=0

for arg in "$@"; do
  case "$arg" in
    --install|-i)
      INSTALL=1
      ;;
    --reload|-r)
      RELOAD=1
      ;;
    --stop-existing|-s)
      STOP_EXISTING=1
      ;;
    *)
      echo "Opcion desconocida: $arg"
      echo "Uso: ./scripts/dev.sh [--install] [--reload] [--stop-existing]"
      exit 1
      ;;
  esac
done

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$ROOT/erma/backend"
FRONTEND_DIR="$ROOT/erma/frontend"
LOGS_DIR="$ROOT/.logs"
PYTHON_EXE="$BACKEND_DIR/.venv/bin/python"

mkdir -p "$LOGS_DIR"

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

stop_port() {
  local port="$1"

  if command_exists lsof; then
    local pids
    pids="$(lsof -ti tcp:"$port" || true)"
    if [ -n "$pids" ]; then
      echo "Apagando procesos en puerto $port..."
      kill $pids 2>/dev/null || true
      sleep 1
    fi
    return
  fi

  if command_exists fuser; then
    if fuser "$port/tcp" >/dev/null 2>&1; then
      echo "Apagando procesos en puerto $port..."
      fuser -k "$port/tcp" >/dev/null 2>&1 || true
      sleep 1
    fi
  fi
}

check_port() {
  local port="$1"
  local name="$2"

  if command_exists lsof && lsof -ti tcp:"$port" >/dev/null 2>&1; then
    echo "No puedo iniciar $name porque el puerto $port ya esta en uso."
    echo "Ejecuta: ./scripts/dev.sh --stop-existing"
    exit 1
  fi

  if command_exists fuser && fuser "$port/tcp" >/dev/null 2>&1; then
    echo "No puedo iniciar $name porque el puerto $port ya esta en uso."
    echo "Ejecuta: ./scripts/dev.sh --stop-existing"
    exit 1
  fi
}

ensure_backend() {
  if [ ! -x "$PYTHON_EXE" ]; then
    echo "Creando entorno virtual del backend..."
    cd "$BACKEND_DIR"
    python3 -m venv .venv
    INSTALL=1
  fi

  if [ "$INSTALL" -eq 1 ]; then
    echo "Instalando dependencias del backend..."
    cd "$BACKEND_DIR"
    "$PYTHON_EXE" -m pip install -r requirements.txt
  fi
}

ensure_frontend() {
  if [ "$INSTALL" -eq 1 ] || [ ! -d "$FRONTEND_DIR/node_modules" ]; then
    echo "Instalando dependencias del frontend..."
    cd "$FRONTEND_DIR"
    npm install
  fi
}

ensure_backend
ensure_frontend

if [ "$STOP_EXISTING" -eq 1 ]; then
  stop_port 8000
  stop_port 5173
fi

check_port 8000 "backend"
check_port 5173 "frontend"

RUN_ID="$(date +%Y%m%d-%H%M%S)"
BACKEND_OUT="$LOGS_DIR/backend-$RUN_ID.out.log"
BACKEND_ERR="$LOGS_DIR/backend-$RUN_ID.err.log"
FRONTEND_OUT="$LOGS_DIR/frontend-$RUN_ID.out.log"
FRONTEND_ERR="$LOGS_DIR/frontend-$RUN_ID.err.log"

BACKEND_ARGS=("-m" "uvicorn" "app.main:app" "--host" "0.0.0.0" "--port" "8000")

if [ "$RELOAD" -eq 1 ]; then
  BACKEND_ARGS=("-m" "uvicorn" "app.main:app" "--reload" "--host" "0.0.0.0" "--port" "8000")
fi

echo "Iniciando backend..."
cd "$BACKEND_DIR"
"$PYTHON_EXE" "${BACKEND_ARGS[@]}" >"$BACKEND_OUT" 2>"$BACKEND_ERR" &
BACKEND_PID=$!

echo "Iniciando frontend..."
cd "$FRONTEND_DIR"
npm run dev -- --host 0.0.0.0 --port 5173 >"$FRONTEND_OUT" 2>"$FRONTEND_ERR" &
FRONTEND_PID=$!

cleanup() {
  echo ""
  echo "Apagando ERMA..."
  kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
}

trap cleanup EXIT INT TERM

echo ""
echo "ERMA esta corriendo en la Raspberry:"
echo "Frontend local: http://127.0.0.1:5173"
echo "Backend local:  http://127.0.0.1:8000"
echo ""
echo "Desde otra maquina, abri:"
echo "Frontend: http://IP_DE_LA_RASPBERRY:5173"
echo "Backend:  http://IP_DE_LA_RASPBERRY:8000"
echo ""
echo "Logs:"
echo "Backend:  $BACKEND_OUT"
echo "Frontend: $FRONTEND_OUT"
echo ""
echo "Para apagar ERMA, presiona Ctrl+C."

while true; do
  if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
    echo "El backend se detuvo. Revisa $BACKEND_ERR"
    exit 1
  fi

  if ! kill -0 "$FRONTEND_PID" 2>/dev/null; then
    echo "El frontend se detuvo. Revisa $FRONTEND_ERR"
    exit 1
  fi

  sleep 2
done
