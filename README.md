# 🔮 FutureCandle - Indian Stock Market Decision Maker

**AI-Powered Candlestick Pattern Recognition, Sentiment Analysis & Long-Term Investment Recommendation Engine for the Indian Stock Market (NSE/BSE)**

---

## ⚡ One-Command Setup (3 ways)

### Way 1: Shell Script (quickest)
```bash
git clone https://github.com/AfzalAshraf/FutureCandle.git
cd FutureCandle
chmod +x start.sh && ./start.sh
# → Opens at http://localhost:5000
```

### Way 2: Make
```bash
make run          # start on port 5000
make run PORT=8080 # custom port
make stop          # stop
make test          # run API tests
make restart       # restart
```

### Way 3: Docker (one command, zero setup)
```bash
docker compose up -d
# → Opens at http://localhost:5000
```
Or without compose:
```bash
docker build -t futurecandle . && docker run -d -p 5000:5000 futurecandle
```

---

## 🔄 Auto-Update on Every Commit (CI/CD)

FutureCandle uses **GitHub Actions** to auto-deploy on every push to `main`:

### What happens on every commit:
1. ✅ **CI Pipeline** runs all engine tests (candlestick, technical, sentiment, investment)
2. ✅ **API tests** validate all endpoints return correct data
3. ✅ **Docker image** is built & pushed to GitHub Container Registry
4. ✅ **Auto-deploy** to your server (when configured)

### Enable auto-deploy to your server:

1. Go to **GitHub → Settings → Secrets → Actions**
2. Add these secrets:

| Secret | Value |
|--------|-------|
| `DEPLOY_HOST` | Your server IP (e.g. `142.93.x.x`) |
| `DEPLOY_USER` | SSH username (e.g. `ubuntu`) |
| `SSH_PRIVATE_KEY` | Your SSH private key |

3. Uncomment the deploy section in `.github/workflows/deploy.yml`
4. Every `git push origin main` will now auto-deploy!

### Pull the latest image (manual deploy):
```bash
docker pull ghcr.io/AfzalAshraf/FutureCandle:latest
docker stop futurecandle && docker rm futurecandle
docker run -d --name futurecandle -p 5000:5000 --restart unless-stopped \
  ghcr.io/AfzalAshraf/FutureCandle:latest
```

---

## 🎯 What It Does

FutureCandle is a comprehensive stock market analysis platform specifically designed for the **Indian stock market**. It combines multiple analysis techniques to provide:

### 1. 🕯️ Candlestick Pattern Recognition (40+ Patterns)
- **Single Candle:** Doji, Hammer, Hanging Man, Shooting Star, Inverted Hammer, Spinning Top, Marubozu, Dragonfly/Gravestone Doji
- **Two Candle:** Bullish/Bearish Engulfing, Piercing Line, Dark Cloud Cover, Harami, Tweezer Top/Bottom, Kicking, On Neck, In Neck, Thrusting
- **Three Candle:** Morning Star, Evening Star, Three White Soldiers, Three Black Crows, Abandoned Baby, Three Inside/Outside Up/Down, Rising/Falling Three Methods

### 2. 📉 Technical Analysis (25+ Indicators)
- **Trend:** SMA (5/10/20/50/100/200), EMA (9/12/21/26/50), MACD, ADX, Ichimoku Cloud, Supertrend
- **Momentum:** RSI (14), Stochastic Oscillator, Williams %R, CCI, ROC, MFI
- **Volatility:** Bollinger Bands, ATR (Average True Range)
- **Volume:** OBV, VWAP, Volume Analysis
- **Support/Resistance:** Pivot Points, Fibonacci Retracement Levels

### 3. 🧠 Sentiment Analysis
- Market Regime Detection (Bull/Bear/Sideways)
- Fear & Greed Index (0-100)
- Technical Sentiment Scoring
- Pattern Sentiment Aggregation
- Volume Sentiment Analysis
- Momentum Analysis
- Sector-Specific Sentiment (IT, Banking, Pharma, Auto, Energy, Metals, Realty, etc.)

### 4. 💰 Investment Recommendations
- **Strategy Types:** Aggressive Growth, Growth, Balanced, Defensive, Capital Preservation
- **Asset Allocation:** Equity/Debt/Gold/Cash breakdown
- **Market Cap Allocation:** Large/Mid/Small/Micro Cap
- **Entry/Exit Points:** Ideal entry, buy-on-dip, targets, stop-loss, risk-reward ratio
- **Duration:** Minimum, recommended, and optimal holding periods
- **SIP Recommendations:** Frequency, step-up strategy, platform suggestions

### 5. 💎 Wealth Projections
- Lumpsum projections for ₹10K to ₹50L across 1-20 years
- SIP projections for ₹1K to ₹50K/month across 3-25 years
- CAGR calculations for Conservative/Moderate/Aggressive scenarios
- Tax implications (LTCG/STCG for Indian equity)

### 6. ⚠️ Risk Assessment
- Technical risk indicators
- Sector-specific risks
- Market cap risk profiling
- Volatility analysis
- Liquidity assessment

---

## 🚀 How to Use

### Quick Start
```bash
# Install dependencies
pip install flask flask-cors yfinance pandas numpy requests textblob scikit-learn scipy python-dateutil

# Run the application
python app.py

# Open in browser
# http://localhost:5000
```

### API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Main web interface |
| `GET /api/stocks` | List of 66+ Indian stocks (Nifty 50 + popular stocks) |
| `GET /api/analyze/<symbol>` | Full analysis (candlestick + technical + sentiment + investment) |
| `GET /api/quick-signal/<symbol>` | Quick buy/sell signal |

### Example API Calls
```bash
# Full analysis of Reliance Industries
curl http://localhost:5000/api/analyze/RELIANCE.NS

# Quick signal for HAL
curl http://localhost:5000/api/quick-signal/HAL.NS

# List all available stocks
curl http://localhost:5000/api/stocks
```

---

## 📊 Supported Indian Stocks (66+)

### Nifty 50 Components
RELIANCE, TCS, HDFC Bank, Infosys, ICICI Bank, Hindustan Unilever, ITC, SBI, Bharti Airtel, Kotak Bank, L&T, Axis Bank, Wipro, HCL Tech, Asian Paints, Maruti, Sun Pharma, Tata Motors, Titan, UltraTech Cement, NTPC, Power Grid, ONGC, M&M, Tata Steel, JSW Steel, Coal India, Bajaj Finance, Bajaj Finserv, Dr. Reddy's, Cipla, Divi's Labs, Eicher Motors, Hero MotoCorp, Britannia, Nestle India, Tech Mahindra, Adani Enterprises, Adani Ports, Grasim, Hindalco, IndusInd Bank, Tata Consumer, Apollo Hospitals, BPCL, HDFC Life, SBI Life, Bajaj Auto, Trent, HAL, BEL

### Popular Mid/Small Caps
Dabur, Pidilite, Havells, DLF, Godrej Consumer, Marico, Siemens, ABB, BHEL, Zomato, Paytm, Nykaa, Polycab, Deepak Nitrite, Alkem Labs

---

## 🏗️ Architecture

```
FutureCandle/
├── app.py                          # Flask main application
├── requirements.txt                # Python dependencies
├── engine/
│   ├── __init__.py
│   ├── candlestick_patterns.py     # 40+ candlestick pattern detection
│   ├── technical_analysis.py       # 25+ technical indicators
│   ├── sentiment_analysis.py       # Market sentiment engine
│   └── investment_engine.py        # Investment recommendation engine
├── templates/
│   └── index.html                  # Main web interface
└── static/
    ├── css/style.css               # Dark theme UI styling
    └── js/app.js                   # Frontend JavaScript
```

---

## 📈 How the Decision Engine Works

### Scoring System
Each stock gets a composite score (0-100) based on:

1. **Technical Score (40%):** RSI, MACD, Bollinger, Stochastic, ADX, Ichimoku, Supertrend, Volume
2. **Candlestick Score (25%):** Pattern strength, frequency, and type (bullish vs bearish)
3. **Sentiment Score (20%):** Market regime, momentum, Fear & Greed index
4. **Volume Score (15%):** OBV trend, MFI, VWAP, volume momentum

### Signal Generation
| Score Range | Signal | Action |
|-------------|--------|--------|
| 75-100 | STRONG_BUY | Aggressive accumulation |
| 60-74 | BUY | Regular buying recommended |
| 45-59 | HOLD | Wait or accumulate on dips |
| 30-44 | SELL | Reduce exposure |
| 0-29 | STRONG_SELL | Exit or strict stop-losses |

### Indian Market Specifics
- Sector growth rates calibrated to Indian market history
- Tax calculations follow Indian LTCG/STCG rules
- SIP recommendations aligned with Indian mutual fund platforms
- Risk assessment considers SEBI regulations and FPI flows
- Fear & Greed index tuned for NSE/BSE volatility patterns

---

## ⚠️ Disclaimer

This tool provides algorithmic analysis based on technical indicators and historical patterns. This is **NOT financial advice**. Past performance does not guarantee future results. Always consult a SEBI-registered financial advisor before making investment decisions. Stock market investments carry inherent risks. Never invest more than you can afford to lose.

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Data:** yfinance (Yahoo Finance API), Pandas, NumPy
- **Analysis:** Custom candlestick engine, scipy, scikit-learn
- **Frontend:** HTML5, CSS3 (Dark Theme), Chart.js, Vanilla JavaScript
- **Market:** Indian Stock Market (NSE/BSE) focused