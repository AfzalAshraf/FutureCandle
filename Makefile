# ============================================================
#  FutureCandle — Makefile
#  Quick commands:  make run | make docker | make stop | make test
# ============================================================
.PHONY: run stop restart test docker docker-stop logs clean

PORT ?= 5000

# ---- One-command start ----
run:
	@chmod +x start.sh stop.sh
	@./start.sh $(PORT)

# ---- Stop ----
stop:
	@chmod +x stop.sh
	@./stop.sh

# ---- Restart ----
restart: stop run

# ---- Test the API ----
test:
	@echo "🧪  Testing FutureCandle API..."
	@curl -sf http://localhost:$(PORT)/api/stocks | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'✅  /api/stocks  →  {len(d)} stocks')" 2>/dev/null || echo "❌  Server not running"
	@curl -sf http://localhost:$(PORT)/api/quick-signal/RELIANCE.NS | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'✅  /api/quick-signal/RELIANCE.NS  →  {d[\"signal\"]} ({d[\"score\"]})')" 2>/dev/null || true
	@curl -sf http://localhost:$(PORT)/api/analyze/TCS.NS | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'✅  /api/analyze/TCS.NS  →  {d[\"technical_analysis\"][\"signal\"][\"action\"]} | {d[\"sentiment\"][\"overall\"]} | {d[\"investment\"][\"verdict\"][\"verdict\"]}')" 2>/dev/null || true

# ---- Docker ----
docker:
	docker compose up -d --build
	@echo "🐳  FutureCandle running at http://localhost:$(PORT)"

docker-stop:
	docker compose down

# ---- Logs ----
logs:
	@if [ -f server.log ]; then tail -f server.log; else docker compose logs -f; fi

# ---- Clean ----
clean:
	rm -rf .venv __pycache__ engine/__pycache__ .pid server.log
	@echo "🧹  Cleaned"