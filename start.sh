#!/usr/bin/env bash
# ============================================================
#  FutureCandle — One-Command Setup & Launch
#  Usage:  ./start.sh          (default port 5000)
#          ./start.sh 8080      (custom port)
# ============================================================
set -euo pipefail

PORT="${1:-5000}"
DIR="$(cd "$(dirname "$0")" && pwd)"
VENV="$DIR/.venv"
PID_FILE="$DIR/.pid"

# ---- colours ----
G='\033[0;32m'; Y='\033[1;33m'; C='\033[0;36m'; R='\033[0m'
info()  { printf "${C}[INFO]${R}  %s\n" "$*"; }
ok()    { printf "${G}[ OK ]${R}  %s\n" "$*"; }
warn()  { printf "${Y}[WARN]${R}  %s\n" "$*"; }

echo ""
echo "🔮  FutureCandle — Indian Stock Market Decision Maker"
echo "======================================================"
echo ""

# ---- 1. Kill any previous instance ----
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE" 2>/dev/null || true)
    if [ -n "$OLD_PID" ] && kill -0 "$OLD_PID" 2>/dev/null; then
        info "Stopping previous instance (PID $OLD_PID)..."
        kill "$OLD_PID" 2>/dev/null || true
        sleep 1
    fi
    rm -f "$PID_FILE"
fi

# ---- 2. Python check ----
if ! command -v python3 &>/dev/null; then
    echo "❌  python3 not found. Install Python 3.9+ first."
    exit 1
fi
PY_VER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
ok "Python $PY_VER found"

# ---- 3. Virtual environment ----
if [ ! -d "$VENV" ]; then
    info "Creating virtual environment..."
    python3 -m venv "$VENV"
    ok "Virtual environment created"
else
    ok "Virtual environment exists"
fi

# ---- 4. Install / update dependencies ----
info "Installing dependencies..."
"$VENV/bin/pip" install --quiet --upgrade pip
"$VENV/bin/pip" install --quiet -r "$DIR/requirements.txt"
ok "Dependencies installed"

# ---- 5. Launch ----
info "Starting FutureCandle on port $PORT ..."
cd "$DIR"
PORT=$PORT nohup "$VENV/bin/python" app.py > "$DIR/server.log" 2>&1 &
echo $! > "$PID_FILE"

# ---- 6. Wait for server ----
for i in $(seq 1 20); do
    if curl -sf "http://127.0.0.1:$PORT/api/stocks" >/dev/null 2>&1; then
        break
    fi
    sleep 0.5
done

if curl -sf "http://127.0.0.1:$PORT/api/stocks" >/dev/null 2>&1; then
    echo ""
    echo "======================================================"
    ok "FutureCandle is LIVE  🚀"
    echo ""
    echo "   🌐  http://localhost:$PORT"
    echo "   📊  http://localhost:$PORT/api/stocks"
    echo "   📈  http://localhost:$PORT/api/analyze/RELIANCE.NS"
    echo ""
    echo "   Logs:   tail -f $DIR/server.log"
    echo "   Stop:   ./stop.sh"
    echo "======================================================"
    echo ""
else
    echo "❌  Server failed to start. Check $DIR/server.log"
    tail -20 "$DIR/server.log"
    exit 1
fi