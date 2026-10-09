"""
FutureCandle - Indian Stock Market Decision Maker
Main Flask Application
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

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Initialize engines
candle_engine = CandlestickPatternEngine()
tech_engine = TechnicalAnalysisEngine()
sentiment_engine = SentimentAnalysisEngine()
invest_engine = InvestmentEngine()

# Indian stock symbols with sector info
INDIAN_STOCKS = {
    # Nifty 50 stocks
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
    'DRREDDY.NS': {'name': 'Dr. Reddy\'s Laboratories', 'sector': 'Pharma', 'cap': 100000},
    'CIPLA.NS': {'name': 'Cipla Limited', 'sector': 'Pharma', 'cap': 100000},
    'DIVISLAB.NS': {'name': 'Divi\'s Laboratories', 'sector': 'Pharma', 'cap': 120000},
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
    # Popular mid/small caps
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


def get_stock_data(symbol: str, period: str = '2y') -> pd.DataFrame:
    """Fetch stock data from yfinance."""
    import yfinance as yf
    ticker = yf.Ticker(symbol)
    df = ticker.history(period=period)
    return df


def generate_mock_data(symbol: str, days: int = 500) -> pd.DataFrame:
    """Generate realistic mock data for demonstration when yfinance is unavailable."""
    np.random.seed(hash(symbol) % 2**31)

    stock_info = INDIAN_STOCKS.get(symbol, {'name': symbol, 'sector': 'General', 'cap': 100000})

    # Base price based on stock
    base_prices = {
        'RELIANCE.NS': 2500, 'TCS.NS': 3800, 'HDFCBANK.NS': 1600, 'INFY.NS': 1500,
        'ICICIBANK.NS': 1100, 'HINDUNILVR.NS': 2400, 'ITC.NS': 450, 'SBIN.NS': 780,
        'BHARTIARTL.NS': 1200, 'LT.NS': 3500, 'WIPRO.NS': 450, 'HCLTECH.NS': 1600,
        'ASIANPAINT.NS': 2800, 'MARUTI.NS': 10500, 'SUNPHARMA.NS': 1200,
        'TATAMOTORS.NS': 750, 'TITAN.NS': 3200, 'NTPC.NS': 350, 'ONGC.NS': 250,
        'M&M.NS': 2700, 'TATASTEEL.NS': 140, 'JSWSTEEL.NS': 850, 'BAJFINANCE.NS': 7000,
        'DRREDDY.NS': 5500, 'CIPLA.NS': 1400, 'HAL.NS': 4200, 'BEL.NS': 220,
        'ZOMATO.NS': 250, 'DLF.NS': 800, 'TRENT.NS': 5000
    }

    base = base_prices.get(symbol, 1000)
    dates = pd.date_range(end=datetime.now(), periods=days, freq='B')

    # Generate OHLCV with realistic patterns
    trend = np.random.choice([-0.0002, 0, 0.0003], p=[0.3, 0.2, 0.5])
    prices = [base]
    for i in range(1, days):
        change = trend + np.random.normal(0, 0.018)
        prices.append(prices[-1] * (1 + change))

    closes = np.array(prices)
    opens = closes * (1 + np.random.normal(0, 0.005, days))
    highs = np.maximum(opens, closes) * (1 + np.abs(np.random.normal(0, 0.008, days)))
    lows = np.minimum(opens, closes) * (1 - np.abs(np.random.normal(0, 0.008, days)))
    volumes = np.random.lognormal(mean=15, sigma=0.5, size=days).astype(int)

    df = pd.DataFrame({
        'Open': opens,
        'High': highs,
        'Low': lows,
        'Close': closes,
        'Volume': volumes
    }, index=dates)

    return df


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/stocks')
def get_stocks():
    """Get list of available Indian stocks."""
    stocks = []
    for sym, info in INDIAN_STOCKS.items():
        stocks.append({
            'symbol': sym,
            'name': info['name'],
            'sector': info['sector'],
            'cap': info['cap']
        })
    return jsonify(stocks)


@app.route('/api/analyze/<symbol>')
def analyze_stock(symbol):
    """Full stock analysis."""
    period = request.args.get('period', '2y')

    try:
        df = get_stock_data(symbol, period)
        if df.empty:
            raise ValueError("Empty data")
    except Exception:
        df = generate_mock_data(symbol)

    if df.empty or len(df) < 10:
        return jsonify({'error': 'Insufficient data for analysis'}), 400

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
        candlestick_result, stock_info['sector'], stock_info['cap']
    )

    # Prepare chart data (last 120 candles)
    chart_df = df.tail(120)
    chart_data = {
        'dates': [d.strftime('%Y-%m-%d') for d in chart_df.index],
        'opens': [round(float(x), 2) for x in chart_df['Open']],
        'highs': [round(float(x), 2) for x in chart_df['High']],
        'lows': [round(float(x), 2) for x in chart_df['Low']],
        'closes': [round(float(x), 2) for x in chart_df['Close']],
        'volumes': [int(x) for x in chart_df['Volume']]
    }

    # Convert numpy types for JSON serialization
    def convert(obj):
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
        if isinstance(obj, float) and (obj != obj):  # NaN
            return None
        if isinstance(obj, float) and abs(obj) == float('inf'):
            return None
        return obj

    result = {
        'symbol': symbol,
        'name': stock_info['name'],
        'sector': stock_info['sector'],
        'current_price': round(current_price, 2),
        'chart_data': chart_data,
        'candlestick_patterns': convert(candlestick_result),
        'technical_analysis': convert(technical_result),
        'sentiment': convert(sentiment_result),
        'investment': convert(investment_result),
        'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'data_points': len(df)
    }

    return jsonify(result)


@app.route('/api/quick-signal/<symbol>')
def quick_signal(symbol):
    """Quick buy/sell signal."""
    try:
        df = get_stock_data(symbol, '6mo')
        if df.empty:
            raise ValueError("Empty data")
    except Exception:
        df = generate_mock_data(symbol, 120)

    tech = tech_engine.calculate_all(df)
    signal = tech.get('signal', {})

    return jsonify({
        'symbol': symbol,
        'price': round(float(df['Close'].iloc[-1]), 2),
        'signal': signal.get('action', 'HOLD'),
        'score': signal.get('score', 50),
        'confidence': signal.get('confidence', 50)
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)