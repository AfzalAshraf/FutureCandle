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
from engine.data_cache import get_cache

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Initialize engines
candle_engine = CandlestickPatternEngine()
tech_engine = TechnicalAnalysisEngine()
sentiment_engine = SentimentAnalysisEngine()
invest_engine = InvestmentEngine()
cache = get_cache()

# Indian stock symbols with sector info
INDIAN_STOCKS = {
    'RELIANCE.NS': {'name': 'Reliance Industries', 'sector': 'Energy', 'cap': 1700000},
    'TCS.NS': {'name': 'Tata Consultancy Services', 'sector': 'IT', 'cap': 1200000},
    'HDFCBANK.NS': {'name': 'HDFC Bank', 'sector': 'Banking', 'cap': 1100000},
    'INFY.NS': {'name': 'Infosys', 'sector': 'IT', 'cap': 650000},
    'ICICIBANK.NS': {'name': 'ICICI Bank', 'sector': 'Banking', 'cap': 700000},
    'HINDUNILVR.NS': {'name': 'Hindustan Unilever', 'sector': 'FMCG', 'cap': 550000},
    'ITC.NS': {'name': 'ITC Limited', 'sector': 'FMCG', 'cap': 520000},
    'SBIN.NS': {'name': 'State Bank of India', 'sector': 'Banking', 'cap': 500000},
    'BHARTIARTL.NS': {'name': 'Bharti Airtel', 'sector': 'Telecom', 'cap': 480000},
    'KOTAKBANK.NS': {'name': 'Kotak Mahindra Bank', 'sector': 'Banking', 'cap': 350000},
    'LT.NS': {'name': 'Larsen & Toubro', 'sector': 'Infra', 'cap': 400000},
    'AXISBANK.NS': {'name': 'Axis Bank', 'sector': 'Banking', 'cap': 300000},
    'WIPRO.NS': {'name': 'Wipro', 'sector': 'IT', 'cap': 220000},
    'HCLTECH.NS': {'name': 'HCL Technologies', 'sector': 'IT', 'cap': 350000},
    'ASIANPAINT.NS': {'name': 'Asian Paints', 'sector': 'FMCG', 'cap': 250000},
    'MARUTI.NS': {'name': 'Maruti Suzuki', 'sector': 'Auto', 'cap': 350000},
    'SUNPHARMA.NS': {'name': 'Sun Pharma', 'sector': 'Pharma', 'cap': 300000},
    'TATAMOTORS.NS': {'name': 'Tata Motors', 'sector': 'Auto', 'cap': 250000},
    'TITAN.NS': {'name': 'Titan Company', 'sector': 'FMCG', 'cap': 280000},
    'ULTRACEMCO.NS': {'name': 'UltraTech Cement', 'sector': 'Cement', 'cap': 300000},
    'NTPC.NS': {'name': 'NTPC Limited', 'sector': 'Energy', 'cap': 300000},
    'POWERGRID.NS': {'name': 'Power Grid Corp', 'sector': 'Energy', 'cap': 250000},
    'ONGC.NS': {'name': 'Oil & Natural Gas Corp', 'sector': 'Energy', 'cap': 250000},
    'M&M.NS': {'name': 'Mahindra & Mahindra', 'sector': 'Auto', 'cap': 300000},
    'TATASTEEL.NS': {'name': 'Tata Steel', 'sector': 'Metals', 'cap': 180000},
    'JSWSTEEL.NS': {'name': 'JSW Steel', 'sector': 'Metals', 'cap': 200000},
    'COALINDIA.NS': {'name': 'Coal India', 'sector': 'Energy', 'cap': 150000},
    'BAJFINANCE.NS': {'name': 'Bajaj Finance', 'sector': 'Banking', 'cap': 400000},
    'BAJAJFINSV.NS': {'name': 'Bajaj Finserv', 'sector': 'Banking', 'cap': 250000},
    'DRREDDY.NS': {'name': "Dr. Reddy's Laboratories", 'sector': 'Pharma', 'cap': 100000},
    'CIPLA.NS': {'name': 'Cipla Limited', 'sector': 'Pharma', 'cap': 100000},
    'DIVISLAB.NS': {'name': "Divi's Laboratories", 'sector': 'Pharma', 'cap': 120000},
    'EICHERMOT.NS': {'name': 'Eicher Motors', 'sector': 'Auto', 'cap': 100000},
    'HEROMOTOCO.NS': {'name': 'Hero MotoCorp', 'sector': 'Auto', 'cap': 80000},
    'BRITANNIA.NS': {'name': 'Britannia Industries', 'sector': 'FMCG', 'cap': 120000},
    'NESTLEIND.NS': {'name': 'Nestle India', 'sector': 'FMCG', 'cap': 220000},
    'TECHM.NS': {'name': 'Tech Mahindra', 'sector': 'IT', 'cap': 130000},
    'ADANIENT.NS': {'name': 'Adani Enterprises', 'sector': 'Infra', 'cap': 300000},
    'ADANIPORTS.NS': {'name': 'Adani Ports', 'sector': 'Infra', 'cap': 250000},
    'GRASIM.NS': {'name': 'Grasim Industries', 'sector': 'Cement', 'cap': 150000},
    'HINDALCO.NS': {'name': 'Hindalco Industries', 'sector': 'Metals', 'cap': 130000},
    'INDUSINDBK.NS': {'name': 'IndusInd Bank', 'sector': 'Banking', 'cap': 80000},
    'TATACONSUM.NS': {'name': 'Tata Consumer Products', 'sector': 'FMCG', 'cap': 90000},
    'APOLLOHOSP.NS': {'name': 'Apollo Hospitals', 'sector': 'Pharma', 'cap': 70000},
    'BPCL.NS': {'name': 'Bharat Petroleum', 'sector': 'Energy', 'cap': 100000},
    'HDFCLIFE.NS': {'name': 'HDFC Life Insurance', 'sector': 'Banking', 'cap': 130000},
    'SBILIFE.NS': {'name': 'SBI Life Insurance', 'sector': 'Banking', 'cap': 150000},
    'BAJAJ-AUTO.NS': {'name': 'Bajaj Auto', 'sector': 'Auto', 'cap': 200000},
    'TRENT.NS': {'name': 'Trent Limited', 'sector': 'FMCG', 'cap': 180000},
    'HAL.NS': {'name': 'Hindustan Aeronautics', 'sector': 'Defense', 'cap': 250000},
    'BEL.NS': {'name': 'Bharat Electronics', 'sector': 'Defense', 'cap': 180000},
    'DABUR.NS': {'name': 'Dabur India', 'sector': 'FMCG', 'cap': 80000},
    'PIDILITIND.NS': {'name': 'Pidilite Industries', 'sector': 'FMCG', 'cap': 120000},
    'HAVELLS.NS': {'name': 'Havells India', 'sector': 'Energy', 'cap': 80000},
    'DLF.NS': {'name': 'DLF Limited', 'sector': 'Realty', 'cap': 180000},
    'GODREJCP.NS': {'name': 'Godrej Consumer Products', 'sector': 'FMCG', 'cap': 100000},
    'MARICO.NS': {'name': 'Marico Limited', 'sector': 'FMCG', 'cap': 70000},
    'SIEMENS.NS': {'name': 'Siemens India', 'sector': 'Infra', 'cap': 150000},
    'ABB.NS': {'name': 'ABB India', 'sector': 'Infra', 'cap': 100000},
    'BHEL.NS': {'name': 'Bharat Heavy Electricals', 'sector': 'Infra', 'cap': 70000},
    'ZOMATO.NS': {'name': 'Zomato Limited', 'sector': 'IT', 'cap': 150000},
    'PAYTM.NS': {'name': 'One97 Communications (Paytm)', 'sector': 'IT', 'cap': 40000},
    'NYKAA.NS': {'name': 'FSN E-Commerce (Nykaa)', 'sector': 'FMCG', 'cap': 50000},
    'POLYCAB.NS': {'name': 'Polycab India', 'sector': 'Energy', 'cap': 70000},
    'DEEPAKNTR.NS': {'name': 'Deepak Nitrite', 'sector': 'Energy', 'cap': 40000},
    'ALKEM.NS': {'name': 'Alkem Laboratories', 'sector': 'Pharma', 'cap': 60000},
}


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
    stocks = []
    for sym, info in INDIAN_STOCKS.items():
        stocks.append({
            'symbol': sym,
            'name': info['name'],
            'sector': info['sector'],
            'cap': info['cap'],
            'type': 'stock'
        })
    return jsonify(stocks)


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
    else:
        stock_info = INDIAN_STOCKS.get(symbol, {'name': symbol, 'sector': 'General', 'cap': 100000})

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