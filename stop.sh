#!/usr/bin/env bash
# Stop FutureCandle
DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$DIR/.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        kill "$PID"
        echo "✅  FutureCandle stopped (PID $PID)"
    else
        echo "⚠️  Process $PID not running"
    fi
    rm -f "$PID_FILE"
else
    echo "⚠️  No PID file found. Killing any app.py on port 5000..."
    pkill -f "python.*app.py" 2>/dev/null && echo "✅  Killed" || echo "Nothing to kill"
fi