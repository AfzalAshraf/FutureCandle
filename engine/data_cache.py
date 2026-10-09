"""
Data Cache Engine
Fetches & caches all index/stock data, auto-refreshes every N hours
"""
import os
import json
import time
import threading
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".cache")
os.makedirs(CACHE_DIR, exist_ok=True)


class DataCache:
    """
    Thread-safe data cache with auto-refresh.
    Stores OHLCV data for all indices and stocks.
    Refreshes every REFRESH_HOURS (default 5).
    """

    REFRESH_HOURS = 5
    REFRESH_SECONDS = REFRESH_HOURS * 3600

    def __init__(self):
        self._lock = threading.Lock()
        self._data: Dict[str, pd.DataFrame] = {}
        self._last_update: Dict[str, float] = {}
        self._meta: Dict[str, dict] = {}
        self._update_thread: Optional[threading.Thread] = None
        self._running = False

    # ------------------------------------------------------------------
    #  Public API
    # ------------------------------------------------------------------

    def get(self, symbol: str, period: str = "2y") -> Optional[pd.DataFrame]:
        """Get cached data or fetch fresh."""
        with self._lock:
            if self._is_fresh(symbol):
                return self._data.get(symbol)

        # Fetch outside lock
        df = self._fetch(symbol, period)
        if df is not None and not df.empty:
            with self._lock:
                self._data[symbol] = df
                self._last_update[symbol] = time.time()
                self._meta[symbol] = {
                    "rows": len(df),
                    "last_date": str(df.index[-1]),
                    "updated": datetime.now().isoformat()
                }
            return df
        return None

    def get_price(self, symbol: str) -> Optional[float]:
        """Get latest close price."""
        df = self.get(symbol)
        if df is not None and not df.empty:
            return round(float(df["Close"].iloc[-1]), 2)
        return None

    def bulk_refresh(self, symbols: list, period: str = "2y"):
        """Refresh a list of symbols (called by scheduler)."""
        results = {"success": 0, "failed": 0, "errors": []}
        for sym in symbols:
            try:
                df = self._fetch(sym, period)
                if df is not None and not df.empty:
                    with self._lock:
                        self._data[sym] = df
                        self._last_update[sym] = time.time()
                        self._meta[sym] = {
                            "rows": len(df),
                            "last_date": str(df.index[-1]),
                            "updated": datetime.now().isoformat(),
                            "last_price": round(float(df["Close"].iloc[-1]), 2),
                            "prev_close": round(float(df["Close"].iloc[-2]), 2) if len(df) > 1 else None,
                            "change_pct": round(
                                (float(df["Close"].iloc[-1]) - float(df["Close"].iloc[-2]))
                                / float(df["Close"].iloc[-2]) * 100, 2
                            ) if len(df) > 1 else 0,
                        }
                    results["success"] += 1
                else:
                    results["failed"] += 1
                    results["errors"].append(f"{sym}: empty data")
            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"{sym}: {str(e)[:80]}")
        results["timestamp"] = datetime.now().isoformat()
        return results

    def get_all_meta(self) -> Dict[str, dict]:
        """Return metadata for all cached symbols."""
        with self._lock:
            return dict(self._meta)

    def get_cache_status(self) -> dict:
        """Cache health check."""
        with self._lock:
            total = len(self._data)
            now = time.time()
            fresh = sum(1 for t in self._last_update.values()
                        if now - t < self.REFRESH_SECONDS)
            stale = total - fresh
            oldest = min(self._last_update.values()) if self._last_update else 0
            newest = max(self._last_update.values()) if self._last_update else 0
        return {
            "total_cached": total,
            "fresh": fresh,
            "stale": stale,
            "refresh_hours": self.REFRESH_HOURS,
            "oldest_update": datetime.fromtimestamp(oldest).isoformat() if oldest else None,
            "newest_update": datetime.fromtimestamp(newest).isoformat() if newest else None,
        }

    def is_symbol_cached(self, symbol: str) -> bool:
        with self._lock:
            return symbol in self._data and self._is_fresh(symbol)

    # ------------------------------------------------------------------
    #  Scheduler — runs in background thread
    # ------------------------------------------------------------------

    def start_auto_refresh(self, symbols: list, period: str = "2y"):
        """Start background auto-refresh thread."""
        self._running = True
        self._update_thread = threading.Thread(
            target=self._refresh_loop,
            args=(symbols, period),
            daemon=True,
            name="DataCache-Refresh"
        )
        self._update_thread.start()
        print(f"⏰  Auto-refresh started: every {self.REFRESH_HOURS} hours for {len(symbols)} symbols")

    def stop_auto_refresh(self):
        self._running = False

    def _refresh_loop(self, symbols: list, period: str):
        """Background loop — refresh all symbols every REFRESH_HOURS."""
        while self._running:
            try:
                print(f"🔄  [{datetime.now().strftime('%Y-%m-%d %H:%M')}] Refreshing {len(symbols)} symbols...")
                result = self.bulk_refresh(symbols, period)
                print(f"✅  Refresh complete: {result['success']} ok, {result['failed']} failed")

                # Save snapshot to disk
                self._save_snapshot()
            except Exception as e:
                print(f"❌  Refresh error: {e}")

            # Sleep in small increments so we can stop quickly
            for _ in range(self.REFRESH_SECONDS):
                if not self._running:
                    break
                time.sleep(1)

    # ------------------------------------------------------------------
    #  Internal helpers
    # ------------------------------------------------------------------

    def _is_fresh(self, symbol: str) -> bool:
        if symbol not in self._last_update:
            return False
        age = time.time() - self._last_update[symbol]
        return age < self.REFRESH_SECONDS

    def _fetch(self, symbol: str, period: str = "2y") -> Optional[pd.DataFrame]:
        """Try yfinance first, fall back to mock data."""
        try:
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period)
            if df is not None and not df.empty and len(df) > 20:
                return df
        except Exception:
            pass

        # Fallback: mock data for demo/offline
        return self._generate_mock(symbol, period)

    def _generate_mock(self, symbol: str, period: str = "2y") -> pd.DataFrame:
        """Generate realistic mock OHLCV data."""
        days = {"1y": 252, "2y": 504, "6mo": 126, "3mo": 63, "1mo": 22}.get(period, 504)
        seed = sum(ord(c) for c in symbol) % (2**31)
        np.random.seed(seed)

        # Realistic base prices for known indices
        base_prices = {
            "^NSEI": 24500, "^BSESN": 81000, "^CNXIT": 38000, "^NSEBANK": 51000,
            "NIFTY_PHARMA.NS": 20000, "NIFTY_AUTO.NS": 25000, "NIFTY_FMCG.NS": 56000,
            "NIFTY_METAL.NS": 8500, "NIFTY_ENERGY.NS": 38000, "NIFTY_REALTY.NS": 900,
            "NIFTY_INFRA.NS": 8000, "NIFTY_PVT_BANK.NS": 25000, "NIFTY_PSU_BANK.NS": 7000,
            "NIFTY_MEDIA.NS": 2200, "NIFTY_DEFENCE.NS": 7000, "NIFTY_FIN_SERVICE.NS": 23000,
            "NIFTY_HEALTHCARE.NS": 13000, "NIFTY_OIL_GAS.NS": 12000, "NIFTY_COMMODITIES.NS": 8000,
            "^INDIAVIX": 14, "NIFTY_MIDCAP_100.NS": 55000, "NIFTY_SMLCAP_100.NS": 18000,
            "^NSMIDCP": 65000, "NIFTY500.NS": 21000, "NIFTY_MOMENTUM_30.NS": 60000,
            "NIFTY_ALPHA_30.NS": 35000, "NIFTY_LOW_VOLATILITY_50.NS": 28000,
        }
        base = base_prices.get(symbol, 15000)

        # Sector-based volatility
        high_vol = {"NIFTY_METAL.NS", "NIFTY_REALTY.NS", "NIFTY_MEDIA.NS",
                    "NIFTY_DEFENCE.NS", "NIFTY_MOMENTUM_30.NS", "NIFTY_HIGH_BETA_50.NS"}
        low_vol = {"NIFTY_FMCG.NS", "NIFTY_LOW_VOLATILITY_50.NS", "^INDIAVIX",
                   "NIFTY50_EQUAL_WEIGHT.NS", "NIFTY_QUALITY_30.NS"}

        if symbol in high_vol:
            vol = 0.025
        elif symbol in low_vol:
            vol = 0.010
        else:
            vol = 0.015

        # Trend: most Indian indices trend up over long term
        drift = 0.00025
        if "PSU" in symbol or "DEFENCE" in symbol:
            drift = 0.0004  # strong uptrend
        elif "VIX" in symbol:
            drift = -0.0001  # mean-reverting

        dates = pd.date_range(end=datetime.now(), periods=days, freq="B")
        prices = [base]
        for _ in range(1, days):
            change = drift + np.random.normal(0, vol)
            prices.append(prices[-1] * (1 + change))

        closes = np.array(prices)
        opens = closes * (1 + np.random.normal(0, 0.003, days))
        highs = np.maximum(opens, closes) * (1 + np.abs(np.random.normal(0, vol * 0.5, days)))
        lows = np.minimum(opens, closes) * (1 - np.abs(np.random.normal(0, vol * 0.5, days)))
        volumes = np.random.lognormal(mean=18, sigma=0.4, size=days).astype(int)

        return pd.DataFrame({
            "Open": opens, "High": highs, "Low": lows,
            "Close": closes, "Volume": volumes
        }, index=dates)

    def _save_snapshot(self):
        """Save cache metadata to disk for persistence across restarts."""
        try:
            snapshot = {
                "meta": self._meta,
                "last_update": {k: v for k, v in self._last_update.items()},
                "saved_at": datetime.now().isoformat(),
                "refresh_hours": self.REFRESH_HOURS,
            }
            path = os.path.join(CACHE_DIR, "snapshot.json")
            with open(path, "w") as f:
                json.dump(snapshot, f, indent=2, default=str)
        except Exception as e:
            print(f"⚠️  Could not save snapshot: {e}")


# Singleton
_cache = DataCache()


def get_cache() -> DataCache:
    return _cache