"""
FutureCandle - Indian Stock Market Decision Maker
Main Flask Application with Auto-Refresh + All Indices
"""
import json
import os
import numpy as np
import pandas as pd
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta

from engine.candlestick_patterns import CandlestickPatternEngine
from engine.technical_analysis import TechnicalAnalysisEngine
from engine.sentiment_analysis import SentimentAnalysisEngine
from engine.investment_engine import InvestmentEngine
from engine.indices import INDIAN_INDICES, CATEGORIES, SECTORS
from engine.all_stocks import get_all_stocks_flat, SECTOR_STOCKS, get_sector_count
from engine.data_cache import get_cache

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Initialize engines
candle_engine = CandlestickPatternEngine()
tech_engine = TechnicalAnalysisEngine()
sentiment_engine = SentimentAnalysisEngine()
invest_engine = InvestmentEngine()
cache = get_cache()

# Load complete stock database from all_stocks.py (477+ stocks)
INDIAN_STOCKS = get_all_stocks_flat()


def convert(obj):
    """Convert numpy types for JSON serialization."""
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    if isinstance(obj, dict):
        return {str(k): convert(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [convert(v) for v in obj]
    if isinstance(obj, float) and (obj != obj):
        return None
    if isinstance(obj, float) and abs(obj) == float('inf'):
        return None
    return obj


def get_stock_data(symbol: str, period: str = '2y') -> pd.DataFrame:
    """Get data from cache (auto-refreshes every 5 hours)."""
    df = cache.get(symbol, period)
    if df is None or df.empty:
        raise ValueError(f"No data for {symbol}")
    return df


# ==============================================================
#  ROUTES
# ==============================================================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/stocks')
def get_stocks():
    """Get list of all available stocks."""
    sector = request.args.get('sector', '').strip()
    q = request.args.get('q', '').strip().lower()
    stocks = []
    for sym, info in INDIAN_STOCKS.items():
        if sector and info['sector'] != sector:
            continue
        if q and q not in sym.lower() and q not in info['name'].lower() and q not in info['sector'].lower():
            continue
        stocks.append({
            'symbol': sym,
            'name': info['name'],
            'sector': info['sector'],
            'cap': info['cap'],
            'type': 'stock'
        })
    return jsonify(stocks)


@app.route('/api/sectors')
def get_sectors_list():
    """Get all sectors with stock counts."""
    counts = get_sector_count()
    sectors = []
    for sector, count in sorted(counts.items()):
        sectors.append({'name': sector, 'count': count})
    return jsonify(sectors)


@app.route('/api/indices')
def get_indices():
    """Get all Indian indices grouped by category."""
    grouped = {}
    for sym, info in INDIAN_INDICES.items():
        cat = info["category"]
        if cat not in grouped:
            grouped[cat] = []
        price = cache.get_price(sym)
        meta = cache.get_all_meta().get(sym, {})
        grouped[cat].append({
            "symbol": sym,
            "name": info["name"],
            "exchange": info["exchange"],
            "sector": info["sector"],
            "description": info["description"],
            "price": price,
            "change_pct": meta.get("change_pct", 0),
            "last_updated": meta.get("updated"),
            "type": "index"
        })
    return jsonify({
        "categories": grouped,
        "total": len(INDIAN_INDICES),
        "category_names": CATEGORIES,
        "sector_names": SECTORS,
    })


@app.route('/api/all')
def get_all_symbols():
    """Get both stocks and indices in one list."""
    all_items = []

    # Stocks
    for sym, info in INDIAN_STOCKS.items():
        meta = cache.get_all_meta().get(sym, {})
        all_items.append({
            "symbol": sym,
            "name": info["name"],
            "sector": info["sector"],
            "cap": info.get("cap", 0),
            "type": "stock",
            "price": meta.get("last_price"),
            "change_pct": meta.get("change_pct", 0),
        })

    # Indices
    for sym, info in INDIAN_INDICES.items():
        meta = cache.get_all_meta().get(sym, {})
        all_items.append({
            "symbol": sym,
            "name": info["name"],
            "sector": info["sector"],
            "category": info["category"],
            "exchange": info["exchange"],
            "type": "index",
            "price": meta.get("last_price"),
            "change_pct": meta.get("change_pct", 0),
        })

    return jsonify(all_items)


@app.route('/api/cache/status')
def cache_status():
    """Cache health & auto-refresh status."""
    return jsonify(cache.get_cache_status())


@app.route('/api/analyze/<path:symbol>')
def analyze_stock(symbol):
    """Full stock/index analysis."""
    period = request.args.get('period', '2y')

    try:
        df = get_stock_data(symbol, period)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    if len(df) < 10:
        return jsonify({'error': 'Insufficient data for analysis'}), 400

    # Determine if it's an index or stock
    is_index = symbol in INDIAN_INDICES
    if is_index:
        stock_info = {
            'name': INDIAN_INDICES[symbol]['name'],
            'sector': INDIAN_INDICES[symbol]['sector'],
            'cap': 500000  # default for indices
        }
    elif symbol in INDIAN_STOCKS:
        stock_info = INDIAN_STOCKS[symbol]
    else:
        # Dynamic: user typed any symbol — try to resolve name from data
        stock_info = {'name': symbol.replace('.NS','').replace('.BO',''), 'sector': 'General', 'cap': 50000}

    current_price = float(df['Close'].iloc[-1])

    # Run all engines
    candlestick_result = candle_engine.analyze_dataframe(df)
    technical_result = tech_engine.calculate_all(df)
    sentiment_result = sentiment_engine.analyze(
        symbol, current_price, technical_result, candlestick_result, stock_info['sector']
    )
    investment_result = invest_engine.generate_recommendation(
        symbol, current_price, technical_result, sentiment_result,
        candlestick_result, stock_info['sector'], stock_info.get('cap', 100000)
    )

    # Chart data (last 120 candles)
    chart_df = df.tail(120)
    chart_data = {
        'dates': [d.strftime('%Y-%m-%d') for d in chart_df.index],
        'opens': [round(float(x), 2) for x in chart_df['Open']],
        'highs': [round(float(x), 2) for x in chart_df['High']],
        'lows': [round(float(x), 2) for x in chart_df['Low']],
        'closes': [round(float(x), 2) for x in chart_df['Close']],
        'volumes': [int(x) for x in chart_df['Volume']]
    }

    result = {
        'symbol': symbol,
        'name': stock_info['name'],
        'sector': stock_info['sector'],
        'type': 'index' if is_index else 'stock',
        'current_price': round(current_price, 2),
        'chart_data': chart_data,
        'candlestick_patterns': convert(candlestick_result),
        'technical_analysis': convert(technical_result),
        'sentiment': convert(sentiment_result),
        'investment': convert(investment_result),
        'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'data_points': len(df),
        'cache_info': cache.get_cache_status(),
    }

    return jsonify(result)


@app.route('/api/quick-signal/<path:symbol>')
def quick_signal(symbol):
    """Quick buy/sell signal."""
    try:
        df = get_stock_data(symbol, '6mo')
    except Exception:
        return jsonify({'error': f'No data for {symbol}'}), 400

    tech = tech_engine.calculate_all(df)
    signal = tech.get('signal', {})

    return jsonify({
        'symbol': symbol,
        'price': round(float(df['Close'].iloc[-1]), 2),
        'signal': signal.get('action', 'HOLD'),
        'score': signal.get('score', 50),
        'confidence': signal.get('confidence', 50)
    })


# ==============================================================
#  STARTUP — begin auto-refresh on first request
# ==============================================================

_started = False


@app.before_request
def _start_background_refresh():
    global _started
    if not _started:
        _started = True
        # Collect ALL symbols (stocks + indices) for auto-refresh
        all_symbols = list(INDIAN_STOCKS.keys()) + list(INDIAN_INDICES.keys())
        cache.start_auto_refresh(all_symbols, period="2y")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)