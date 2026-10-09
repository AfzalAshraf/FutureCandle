// FutureCandle - Indian Stock Market Decision Maker
// Main Application JavaScript

let selectedSymbol = 'RELIANCE.NS';
let stocksData = [];
let priceChart = null;
let currentChartType = 'line';

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadStocks();
    setupSearch();
});

// Load stocks list
async function loadStocks() {
    try {
        const res = await fetch('/api/stocks');
        stocksData = await res.json();
    } catch (e) {
        console.error('Failed to load stocks:', e);
    }
}

// Setup search
function setupSearch() {
    const input = document.getElementById('stockSearch');
    const dropdown = document.getElementById('stockDropdown');

    input.addEventListener('input', () => {
        const q = input.value.toLowerCase().trim();
        if (q.length < 1) {
            dropdown.classList.remove('show');
            return;
        }

        const filtered = stocksData.filter(s =>
            s.symbol.toLowerCase().includes(q) ||
            s.name.toLowerCase().includes(q) ||
            s.sector.toLowerCase().includes(q)
        ).slice(0, 15);

        if (filtered.length === 0) {
            dropdown.classList.remove('show');
            return;
        }

        dropdown.innerHTML = filtered.map(s => `
            <div class="stock-dropdown-item" onclick="selectStock('${s.symbol}', '${s.name}', '${s.sector}')">
                <div>
                    <span class="sym">${s.symbol.replace('.NS', '')}</span>
                    <span class="name"> — ${s.name}</span>
                </div>
                <span class="sector-badge">${s.sector}</span>
            </div>
        `).join('');
        dropdown.classList.add('show');
    });

    input.addEventListener('focus', () => {
        if (input.value.length > 0) {
            input.dispatchEvent(new Event('input'));
        }
    });

    document.addEventListener('click', (e) => {
        if (!e.target.closest('.search-wrapper')) {
            dropdown.classList.remove('show');
        }
    });
}

// Select stock
function selectStock(symbol, name, sector) {
    selectedSymbol = symbol;
    document.getElementById('stockSearch').value = '';
    document.getElementById('stockDropdown').classList.remove('show');

    const el = document.getElementById('selectedStock');
    el.querySelector('.stock-symbol').textContent = symbol.replace('.NS', '');
    el.querySelector('.stock-name').textContent = name;
    el.querySelector('.stock-sector').textContent = sector;
}

// Analyze stock
async function analyzeStock() {
    const btn = document.getElementById('analyzeBtn');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');

    btn.disabled = true;
    btn.innerHTML = '<span class="btn-icon">⏳</span> Analyzing...';
    results.classList.add('hidden');
    loading.classList.remove('hidden');

    try {
        const res = await fetch(`/api/analyze/${selectedSymbol}`);
        const data = await res.json();

        if (data.error) {
            alert(data.error);
            return;
        }

        renderResults(data);
        results.classList.remove('hidden');
        results.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (e) {
        console.error('Analysis failed:', e);
        alert('Analysis failed. Please try again.');
    } finally {
        loading.classList.add('hidden');
        btn.disabled = false;
        btn.innerHTML = '<span class="btn-icon">⚡</span> Analyze Now';
    }
}

// Render all results
function renderResults(data) {
    renderVerdict(data.investment, data.current_price);
    renderSignal(data.technical_analysis, data.current_price);
    renderSentiment(data.sentiment);
    renderChart(data.chart_data, data.candlestick_patterns);
    renderTechnical(data.technical_analysis);
    renderPatterns(data.candlestick_patterns);
    renderInvestment(data.investment);
    renderTargets(data.investment.price_targets, data.current_price);
    renderRisks(data.investment.risks);
    renderSIP(data.investment.sip);
    renderProjections(data.investment.projections);
}

// Render Verdict
function renderVerdict(inv, price) {
    const v = inv.verdict;
    const d = inv.duration;
    const el = document.getElementById('verdictContent');

    const starStr = '★'.repeat(v.stars) + '☆'.repeat(5 - v.stars);
    const color = v.stars >= 4 ? 'text-green' : v.stars >= 3 ? 'text-yellow' : 'text-red';

    el.innerHTML = `
        <div class="verdict-stars ${color}">${starStr}</div>
        <div class="verdict-text ${color}">${v.verdict}</div>
        <div style="margin: 12px 0;">
            <div style="display: flex; gap: 16px; flex-wrap: wrap;">
                <div>
                    <span class="text-muted" style="font-size:12px;">CURRENT PRICE</span>
                    <div style="font-size:22px; font-weight:700;">₹${price.toLocaleString('en-IN', {minimumFractionDigits:2})}</div>
                </div>
                <div>
                    <span class="text-muted" style="font-size:12px;">5Y TARGET</span>
                    <div style="font-size:22px; font-weight:700;" class="text-green">${v.target_5_year}</div>
                </div>
                <div>
                    <span class="text-muted" style="font-size:12px;">10Y TARGET</span>
                    <div style="font-size:22px; font-weight:700;" class="text-cyan">${v.target_10_year}</div>
                </div>
                <div>
                    <span class="text-muted" style="font-size:12px;">EXPECTED CAGR</span>
                    <div style="font-size:22px; font-weight:700;" class="text-purple">${v.expected_cagr}</div>
                </div>
            </div>
        </div>
        <div class="verdict-timing">
            <strong>⏰ ${v.timing}</strong><br>
            Recommended Duration: ${v.recommended_duration}
        </div>
        <p style="font-size:12px; color:var(--text-muted); margin-top:12px;">${v.key_message}</p>
    `;
}

// Render Signal
function renderSignal(tech, price) {
    const sig = tech.signal;
    const el = document.getElementById('signalContent');
    const score = sig.score;

    let color, colorClass;
    if (score >= 60) { color = '#10b981'; colorClass = 'text-green'; }
    else if (score >= 40) { color = '#f59e0b'; colorClass = 'text-yellow'; }
    else { color = '#ef4444'; colorClass = 'text-red'; }

    const sr = tech.support_resistance || {};

    el.innerHTML = `
        <div class="signal-big ${colorClass}">${sig.action.replace('_', ' ')}</div>
        <div class="signal-score-bar">
            <div class="signal-score-fill" style="width:${score}%; background:${color};"></div>
        </div>
        <div style="text-align:center; font-size:13px; color:var(--text-muted);">
            Score: ${score}/100 | Confidence: ${sig.confidence}%
        </div>
        <div class="signal-details">
            <div class="signal-detail">
                <div class="label">RSI</div>
                <div class="value">${tech.rsi?.value || 'N/A'}</div>
            </div>
            <div class="signal-detail">
                <div class="label">MACD</div>
                <div class="value" style="font-size:12px;">${tech.macd?.signal_type?.replace('_', ' ') || 'N/A'}</div>
            </div>
            <div class="signal-detail">
                <div class="label">Support</div>
                <div class="value text-green" style="font-size:14px;">₹${sr.nearest_support?.toLocaleString('en-IN') || 'N/A'}</div>
            </div>
            <div class="signal-detail">
                <div class="label">Resistance</div>
                <div class="value text-red" style="font-size:14px;">₹${sr.nearest_resistance?.toLocaleString('en-IN') || 'N/A'}</div>
            </div>
        </div>
    `;
}

// Render Sentiment
function renderSentiment(sent) {
    const el = document.getElementById('sentimentContent');
    const fg = sent.fear_greed_index;

    el.innerHTML = `
        <div class="sentiment-gauge">
            <div class="sentiment-emoji">${sent.emoji}</div>
            <div class="sentiment-label">${sent.overall.replace('_', ' ')}</div>
            <div class="sentiment-score" style="color: ${sent.composite_score > 55 ? '#10b981' : sent.composite_score > 40 ? '#f59e0b' : '#ef4444'}">
                ${sent.composite_score}/100
            </div>
        </div>
        <div style="margin-top:16px;">
            <div style="font-size:12px; color:var(--text-muted); margin-bottom:4px;">FEAR & GREED INDEX</div>
            <div class="fear-greed-bar">
                <div class="fear-greed-marker" style="left:${fg.index}%"></div>
            </div>
            <div class="fear-greed-labels">
                <span>EXTREME FEAR</span>
                <span>NEUTRAL</span>
                <span>EXTREME GREED</span>
            </div>
            <div class="fear-greed-zone">
                <div style="font-size:16px; font-weight:700;">${fg.zone.replace('_', ' ')}</div>
                <div class="fear-greed-warning">${fg.warning}</div>
            </div>
        </div>
        <div style="margin-top:16px;">
            <div style="font-size:12px; color:var(--text-muted); margin-bottom:8px;">RECOMMENDATION</div>
            <div style="padding:10px; background:var(--bg-secondary); border-radius:8px; border-left:3px solid var(--accent-purple);">
                <div style="font-weight:600; font-size:14px;">${sent.recommendation.action.replace(/_/g, ' ')}</div>
                <div style="font-size:12px; color:var(--text-secondary); margin-top:4px;">${sent.recommendation.message}</div>
                <div style="font-size:12px; color:var(--accent-cyan); margin-top:4px;">Suggested Position: ${sent.recommendation.suggested_position_pct}% of capital</div>
            </div>
        </div>
    `;
}

// Render Chart
function renderChart(chartData, patterns) {
    const ctx = document.getElementById('priceChart').getContext('2d');

    if (priceChart) priceChart.destroy();

    const labels = chartData.dates;
    const closes = chartData.closes;

    // Create annotation points for recent patterns
    const recentPatterns = (patterns.recent_patterns || []).slice(-10);
    const patternDates = recentPatterns.map(p => p.date?.split(' ')[0]);

    const datasets = [{
        label: 'Close Price (₹)',
        data: closes,
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: true,
        tension: 0.3,
        pointRadius: 0,
        pointHoverRadius: 6,
        borderWidth: 2,
    }];

    // Add moving averages
    if (closes.length >= 20) {
        const sma20 = calculateSMA(closes, 20);
        datasets.push({
            label: 'SMA 20',
            data: sma20,
            borderColor: '#f59e0b',
            borderWidth: 1,
            borderDash: [5, 5],
            pointRadius: 0,
            fill: false,
        });
    }

    if (closes.length >= 50) {
        const sma50 = calculateSMA(closes, 50);
        datasets.push({
            label: 'SMA 50',
            data: sma50,
            borderColor: '#8b5cf6',
            borderWidth: 1,
            borderDash: [5, 5],
            pointRadius: 0,
            fill: false,
        });
    }

    // Bollinger Bands
    if (closes.length >= 20) {
        const { upper, lower } = calculateBollinger(closes, 20);
        datasets.push({
            label: 'BB Upper',
            data: upper,
            borderColor: 'rgba(239, 68, 68, 0.3)',
            borderWidth: 1,
            pointRadius: 0,
            fill: false,
        });
        datasets.push({
            label: 'BB Lower',
            data: lower,
            borderColor: 'rgba(16, 185, 129, 0.3)',
            borderWidth: 1,
            pointRadius: 0,
            fill: '+1',
            backgroundColor: 'rgba(100, 116, 139, 0.05)',
        });
    }

    priceChart = new Chart(ctx, {
        type: 'line',
        data: { labels, datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: { color: '#94a3b8', font: { size: 11 }, usePointStyle: true, pointStyle: 'line' }
                },
                tooltip: {
                    backgroundColor: '#1a2332',
                    titleColor: '#e2e8f0',
                    bodyColor: '#94a3b8',
                    borderColor: '#2d3748',
                    borderWidth: 1,
                    callbacks: {
                        label: (ctx) => `${ctx.dataset.label}: ₹${ctx.parsed.y.toLocaleString('en-IN', {minimumFractionDigits:2})}`
                    }
                }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(45, 55, 72, 0.5)' },
                    ticks: { color: '#64748b', maxTicksLimit: 12, font: { size: 10 } }
                },
                y: {
                    grid: { color: 'rgba(45, 55, 72, 0.5)' },
                    ticks: {
                        color: '#64748b',
                        callback: (v) => '₹' + v.toLocaleString('en-IN')
                    }
                }
            }
        }
    });
}

// Calculate SMA
function calculateSMA(data, period) {
    const result = new Array(data.length).fill(null);
    for (let i = period - 1; i < data.length; i++) {
        let sum = 0;
        for (let j = 0; j < period; j++) sum += data[i - j];
        result[i] = sum / period;
    }
    return result;
}

// Calculate Bollinger Bands
function calculateBollinger(data, period) {
    const upper = new Array(data.length).fill(null);
    const lower = new Array(data.length).fill(null);
    for (let i = period - 1; i < data.length; i++) {
        const slice = data.slice(i - period + 1, i + 1);
        const mean = slice.reduce((a, b) => a + b, 0) / period;
        const std = Math.sqrt(slice.reduce((a, b) => a + (b - mean) ** 2, 0) / period);
        upper[i] = mean + 2 * std;
        lower[i] = mean - 2 * std;
    }
    return { upper, lower };
}

// Set chart type
function setChartType(type) {
    currentChartType = type;
    document.querySelectorAll('.chart-btn').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
    // Chart type toggle - for now line only, candlestick needs more setup
}

// Render Technical Indicators
function renderTechnical(tech) {
    const el = document.getElementById('techContent');
    const items = [];

    const add = (name, value, signal, type) => {
        items.push({ name, value, signal, type: type || 'neutral' });
    };

    // RSI
    const rsi = tech.rsi || {};
    add('RSI (14)', rsi.value, rsi.signal, rsi.value > 50 ? 'bullish' : 'bearish');

    // MACD
    const macd = tech.macd || {};
    add('MACD', macd.histogram?.toFixed(4), macd.signal_type?.replace(/_/g, ' '), macd.signal_type?.includes('BULL') ? 'bullish' : 'bearish');

    // Stochastic
    const stoch = tech.stochastic || {};
    add('Stochastic %K', stoch.k, stoch.signal, stoch.k > 50 ? 'bullish' : 'bearish');

    // ADX
    const adx = tech.adx || {};
    add('ADX', adx.value, `${adx.trend} ${adx.direction}`, adx.direction === 'BULLISH' ? 'bullish' : 'bearish');

    // Bollinger
    const bb = tech.bollinger_bands || {};
    add('Bollinger', `${bb.price_position}%`, bb.signal, bb.signal === 'OVERSOLD' ? 'bullish' : bb.signal === 'OVERBOUGHT' ? 'bearish' : 'neutral');

    // ATR
    const atr = tech.atr || {};
    add('ATR', `₹${atr.value} (${atr.percentage}%)`, `Volatility: ${atr.volatility}`, 'neutral');

    // VWAP
    const vwap = tech.vwap || {};
    add('VWAP', `₹${vwap.value}`, vwap.signal, vwap.signal === 'BULLISH' ? 'bullish' : 'bearish');

    // Williams %R
    const wr = tech.williams_r || {};
    add('Williams %R', wr.value, wr.signal, wr.value > -50 ? 'bullish' : 'bearish');

    // CCI
    const cci = tech.cci || {};
    add('CCI', cci.value, cci.signal, cci.value > 0 ? 'bullish' : 'bearish');

    // MFI
    const mfi = tech.mfi || {};
    add('MFI', mfi.value, mfi.signal, mfi.value > 50 ? 'bullish' : 'bearish');

    // ROC
    const roc = tech.roc || {};
    add('ROC (12)', `${roc.value}%`, roc.signal, roc.value > 0 ? 'bullish' : 'bearish');

    // Ichimoku
    const ichi = tech.ichimoku || {};
    add('Ichimoku', ichi.signal?.replace(/_/g, ' '), ichi.tk_cross, ichi.signal === 'BULLISH' ? 'bullish' : ichi.signal === 'BEARISH' ? 'bearish' : 'neutral');

    // Supertrend
    const st = tech.supertrend || {};
    add('Supertrend', st.signal, `U:${st.upper_band} L:${st.lower_band}`, st.signal === 'BULLISH' ? 'bullish' : st.signal === 'BEARISH' ? 'bearish' : 'neutral');

    // Moving Averages
    const ma = tech.moving_averages || {};
    if (ma.SMA_20) add('SMA 20', `₹${ma.SMA_20}`, ma.SMA_20_signal, ma.SMA_20_signal === 'BULLISH' ? 'bullish' : 'bearish');
    if (ma.SMA_50) add('SMA 50', `₹${ma.SMA_50}`, ma.SMA_50_signal, ma.SMA_50_signal === 'BULLISH' ? 'bullish' : 'bearish');
    if (ma.SMA_200) add('SMA 200', `₹${ma.SMA_200}`, ma.SMA_200_signal, ma.SMA_200_signal === 'BULLISH' ? 'bullish' : 'bearish');
    if (ma.EMA_9) add('EMA 9', `₹${ma.EMA_9}`, ma.EMA_9_signal, ma.EMA_9_signal === 'BULLISH' ? 'bullish' : 'bearish');
    if (ma.cross_signal) add('Golden/Death Cross', '', ma.cross_signal, ma.cross_signal.includes('GOLDEN') ? 'bullish' : 'bearish');

    el.innerHTML = `<div class="tech-grid">${items.map(item => `
        <div class="tech-item ${item.type}">
            <div class="tech-name">${item.name}</div>
            <div class="tech-value">${item.value}</div>
            <div class="tech-signal text-${item.type === 'bullish' ? 'green' : item.type === 'bearish' ? 'red' : 'yellow'}">${item.signal}</div>
        </div>
    `).join('')}</div>`;
}

// Render Patterns
function renderPatterns(data) {
    const el = document.getElementById('patternsContent');
    const recent = data.recent_patterns || [];
    const signal = data.signal || 'NEUTRAL';
    const bullScore = data.bullish_score || 50;
    const bearScore = data.bearish_score || 50;

    let signalColor = signal === 'BULLISH' ? 'text-green' : signal === 'BEARISH' ? 'text-red' : 'text-yellow';

    let html = `
        <div style="margin-bottom:16px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <span class="${signalColor}" style="font-size:18px; font-weight:700;">${signal}</span>
                <span style="font-size:12px; color:var(--text-muted);">${data.total_patterns_detected} patterns detected</span>
            </div>
            <div style="display:flex; gap:8px;">
                <div style="flex:${bullScore}; height:8px; background:var(--accent-green); border-radius:4px;"></div>
                <div style="flex:${bearScore}; height:8px; background:var(--accent-red); border-radius:4px;"></div>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:11px; margin-top:4px;">
                <span class="text-green">Bullish ${bullScore}%</span>
                <span class="text-red">Bearish ${bearScore}%</span>
            </div>
        </div>
    `;

    if (recent.length > 0) {
        html += '<div class="pattern-list">';
        recent.slice(-15).reverse().forEach(p => {
            const icon = p.type === 'bullish' ? '🟢' : p.type === 'bearish' ? '🔴' : '🟡';
            html += `
                <div class="pattern-item">
                    <div class="pattern-icon ${p.type}">${icon}</div>
                    <div class="pattern-info">
                        <div class="pattern-name">${p.pattern.replace(/_/g, ' ')}</div>
                        <div class="pattern-date">${p.date?.split(' ')[0] || ''} | ₹${p.price?.toLocaleString('en-IN') || ''}</div>
                    </div>
                    <span class="pattern-strength ${p.type}">${p.type.toUpperCase()} ${(p.strength * 100).toFixed(0)}%</span>
                </div>
            `;
        });
        html += '</div>';
    } else {
        html += '<p style="color:var(--text-muted); text-align:center; padding:20px;">No recent patterns detected</p>';
    }

    el.innerHTML = html;
}

// Render Investment Details
function renderInvestment(inv) {
    const el = document.getElementById('investmentContent');
    const s = inv.strategy;
    const a = inv.allocation;
    const ee = inv.entry_exit;

    let html = `
        <div class="invest-grid">
            <div class="invest-box">
                <h4>📊 Strategy</h4>
                <div class="big-value text-blue">${s.type.replace(/_/g, ' ')}</div>
                <p>${s.description}</p>
                <p style="margin-top:8px;"><strong>Risk Appetite:</strong> ${s.risk_appetite}</p>
            </div>
            <div class="invest-box">
                <h4>💳 Investment Mode</h4>
                <div class="big-value text-purple" style="font-size:18px;">${s.investment_mode}</div>
                <p>${s.mode_reason}</p>
            </div>
            <div class="invest-box">
                <h4>🎯 Entry & Exit Points</h4>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; font-size:13px;">
                    <div><span class="text-muted">Ideal Entry:</span> <span class="text-green">₹${ee.ideal_entry?.toLocaleString('en-IN')}</span></div>
                    <div><span class="text-muted">Target 1:</span> <span class="text-green">₹${ee.target_1?.toLocaleString('en-IN')}</span></div>
                    <div><span class="text-muted">Buy on Dip:</span> <span class="text-cyan">₹${ee.buy_on_dip?.toLocaleString('en-IN')}</span></div>
                    <div><span class="text-muted">Target 2:</span> <span class="text-green">₹${ee.target_2?.toLocaleString('en-IN')}</span></div>
                    <div><span class="text-muted">Stop Loss:</span> <span class="text-red">₹${ee.stop_loss?.toLocaleString('en-IN')} (${ee.stop_loss_pct}%)</span></div>
                    <div><span class="text-muted">R:R Ratio:</span> <span class="text-yellow">${ee.risk_reward_ratio}</span></div>
                </div>
            </div>
        </div>

        <div style="margin-top:20px;">
            <h4 style="font-size:14px; margin-bottom:12px; color:var(--text-secondary);">💼 Asset Allocation</h4>
            ${renderAllocBar('Equity', a.asset_allocation.equity, '#3b82f6')}
            ${renderAllocBar('Debt / Bonds', a.asset_allocation.debt, '#10b981')}
            ${renderAllocBar('Gold', a.asset_allocation.gold, '#f59e0b')}
            ${renderAllocBar('Cash / Liquid', a.asset_allocation.cash, '#64748b')}
        </div>

        <div style="margin-top:20px;">
            <h4 style="font-size:14px; margin-bottom:12px; color:var(--text-secondary);">📐 Market Cap Allocation</h4>
            ${renderAllocBar('Large Cap', a.cap_allocation.large_cap, '#3b82f6')}
            ${renderAllocBar('Mid Cap', a.cap_allocation.mid_cap, '#8b5cf6')}
            ${renderAllocBar('Small Cap', a.cap_allocation.small_cap, '#f59e0b')}
            ${renderAllocBar('Micro Cap', a.cap_allocation.micro_cap, '#ef4444')}
        </div>

        <div style="margin-top:20px;">
            <h4 style="font-size:14px; margin-bottom:8px; color:var(--text-secondary);">🏭 Sector Recommendations</h4>
            <div class="sector-tags">
                ${a.sector_suggestions.map(s => `
                    <div class="sector-tag">
                        <span class="weight">${s.weight}%</span> ${s.sector}
                        <span style="color:var(--text-muted); font-size:10px;"> — ${s.reason}</span>
                    </div>
                `).join('')}
            </div>
        </div>
    `;

    el.innerHTML = html;
}

function renderAllocBar(label, value, color) {
    return `
        <div class="alloc-bar-group">
            <div class="alloc-bar-label">
                <span>${label}</span>
                <span style="font-weight:700; color:${color};">${value}%</span>
            </div>
            <div class="alloc-bar">
                <div class="alloc-bar-fill" style="width:${value}%; background:${color};"></div>
            </div>
        </div>
    `;
}

// Render Targets
function renderTargets(targets, price) {
    const el = document.getElementById('targetsContent');

    const scenarios = ['conservative', 'moderate', 'aggressive'];
    const timeframes = ['1Y', '3Y', '5Y', '7Y', '10Y', '15Y', '20Y'];
    const colors = { conservative: '#10b981', moderate: '#3b82f6', aggressive: '#f59e0b' };

    let html = `
        <div style="overflow-x:auto;">
        <table class="targets-table">
            <thead>
                <tr>
                    <th>Scenario</th>
                    ${timeframes.map(t => `<th>${t}</th>`).join('')}
                </tr>
            </thead>
            <tbody>
    `;

    scenarios.forEach(scenario => {
        const s = targets[scenario] || {};
        html += `<tr><td style="font-weight:600; color:${colors[scenario]};">${scenario.toUpperCase()}</td>`;
        timeframes.forEach(tf => {
            const t = s[tf];
            if (t) {
                const returnPct = t.return_pct;
                html += `<td>
                    <div style="font-weight:600;">₹${t.price?.toLocaleString('en-IN', {maximumFractionDigits:0})}</div>
                    <div style="font-size:11px; color:var(--text-muted);">+${returnPct}% (${t.cagr}% CAGR)</div>
                </td>`;
            } else {
                html += '<td>—</td>';
            }
        });
        html += '</tr>';
    });

    html += '</tbody></table></div>';

    // Near-term targets
    const nt = targets.near_term || {};
    html += `
        <div style="margin-top:20px;">
            <h4 style="font-size:14px; margin-bottom:12px; color:var(--text-secondary);">📅 Near-Term Targets</h4>
            <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(180px, 1fr)); gap:12px;">
                ${renderNearTerm('3M Bull', nt['3_month_bull'], '#10b981')}
                ${renderNearTerm('3M Bear', nt['3_month_bear'], '#ef4444')}
                ${renderNearTerm('6M Bull', nt['6_month_bull'], '#10b981')}
                ${renderNearTerm('6M Bear', nt['6_month_bear'], '#ef4444')}
                ${renderNearTerm('1Y Bull', nt['1_year_bull'], '#10b981')}
                ${renderNearTerm('1Y Bear', nt['1_year_bear'], '#ef4444')}
            </div>
        </div>
    `;

    el.innerHTML = html;
}

function renderNearTerm(label, value, color) {
    return `
        <div style="padding:12px; background:var(--bg-secondary); border-radius:8px; border-top:2px solid ${color};">
            <div style="font-size:11px; color:var(--text-muted);">${label}</div>
            <div style="font-size:18px; font-weight:700; color:${color};">₹${value?.toLocaleString('en-IN', {maximumFractionDigits:0}) || 'N/A'}</div>
        </div>
    `;
}

// Render Risks
function renderRisks(risks) {
    const el = document.getElementById('riskContent');
    const items = risks.individual_risks || [];

    let html = `
        <div style="margin-bottom:16px; padding:12px; background:var(--bg-secondary); border-radius:8px; display:flex; gap:16px; align-items:center;">
            <span style="font-size:14px; color:var(--text-muted);">Overall Risk Level:</span>
            <span style="font-size:20px; font-weight:700;" class="risk-level ${risks.overall_risk_level.toLowerCase().replace('_', '-')}">${risks.overall_risk_level.replace('_', ' ')}</span>
            <span style="font-size:12px; color:var(--text-muted);">
                (${risks.risk_count?.high || 0} High, ${risks.risk_count?.medium || 0} Medium, ${risks.risk_count?.low || 0} Low)
            </span>
        </div>
        <div class="risk-list">
    `;

    items.forEach(r => {
        const level = r.level.toLowerCase();
        html += `
            <div class="risk-item ${level}">
                <span class="risk-level ${level}">${r.level}</span>
                <div>
                    <div class="risk-type">${r.type}</div>
                    <div class="risk-detail">${r.detail}</div>
                </div>
            </div>
        `;
    });

    html += '</div>';
    el.innerHTML = html;
}

// Render SIP
function renderSIP(sip) {
    const el = document.getElementById('sipContent');

    let html = `
        <div style="margin-bottom:20px; padding:16px; background:var(--bg-secondary); border-radius:8px; border-left:3px solid var(--accent-cyan);">
            <div style="font-size:14px; font-weight:600; margin-bottom:8px;">📅 SIP Recommendations</div>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; font-size:13px;">
                <div><span class="text-muted">Frequency:</span> ${sip.recommended_frequency}</div>
                <div><span class="text-muted">Income Allocation:</span> <span class="text-green">${sip.income_allocation_pct}%</span></div>
                <div><span class="text-muted">Duration:</span> ${sip.duration}</div>
                <div><span class="text-muted">Best SIP Day:</span> ${sip.best_day}</div>
                <div><span class="text-muted">Min Investment:</span> ${sip.minimum_investment}</div>
                <div><span class="text-muted">Auto-invest:</span> ${sip.auto_invest}</div>
            </div>
            ${sip.step_up ? `<div style="margin-top:8px; font-size:12px; color:var(--text-secondary);">
                💡 <strong>Step-Up SIP:</strong> ${sip.step_up.note}
            </div>` : ''}
            ${sip.platforms ? `<div style="margin-top:8px; font-size:12px; color:var(--text-muted);">
                Platforms: ${sip.platforms.join(' • ')}
            </div>` : ''}
        </div>
    `;

    el.innerHTML = html;
}

// Global investment data for projections
let currentInvestmentData = null;

// Override renderResults to store investment data
const _origRenderResults = renderResults;
renderResults = function(data) {
    currentInvestmentData = data.investment;
    _origRenderResults(data);
};

// Render Projections
function renderProjections(proj) {
    if (!proj) return;
    const el = document.getElementById('projectionsContent');
    const lumpsum = proj.lumpsum || {};
    const sip = proj.sip || {};

    let html = `
        <div style="margin-bottom:20px;">
            <h4 style="font-size:15px; margin-bottom:12px; color:var(--accent-green);">💰 Lumpsum Investment Growth</h4>
            <div style="overflow-x:auto;">
                <table class="targets-table">
                    <thead>
                        <tr>
                            <th>Investment</th>
                            <th>1Y</th>
                            <th>3Y</th>
                            <th>5Y</th>
                            <th>7Y</th>
                            <th>10Y</th>
                            <th>15Y</th>
                            <th>20Y</th>
                        </tr>
                    </thead>
                    <tbody>
    `;

    const showAmounts = ['₹10,000', '₹50,000', '₹1,00,000', '₹5,00,000', '₹10,00,000', '₹50,00,000'];
    showAmounts.forEach(amt => {
        const data = lumpsum[amt];
        if (!data) return;
        html += `<tr><td style="font-weight:600; white-space:nowrap;">${amt}</td>`;
        ['1Y', '3Y', '5Y', '7Y', '10Y', '15Y', '20Y'].forEach(years => {
            const d = data[years];
            if (d) {
                html += `<td>
                    <div style="font-weight:600; font-size:13px;">₹${d.future_value.toLocaleString('en-IN', {maximumFractionDigits:0})}</div>
                    <div style="font-size:10px; color:var(--accent-green);">+${d.multiplier}x</div>
                </td>`;
            } else {
                html += '<td>—</td>';
            }
        });
        html += '</tr>';
    });

    html += '</tbody></table></div></div>';

    // SIP Projections
    html += `
        <div>
            <h4 style="font-size:15px; margin-bottom:12px; color:var(--accent-cyan);">📈 Monthly SIP Wealth Creation</h4>
            <div style="overflow-x:auto;">
                <table class="targets-table">
                    <thead>
                        <tr>
                            <th>Monthly SIP</th>
                            <th>3Y</th>
                            <th>5Y</th>
                            <th>7Y</th>
                            <th>10Y</th>
                            <th>15Y</th>
                            <th>20Y</th>
                            <th>25Y</th>
                        </tr>
                    </thead>
                    <tbody>
    `;

    const showSips = ['₹1,000/month', '₹5,000/month', '₹10,000/month', '₹25,000/month', '₹50,000/month'];
    showSips.forEach(amt => {
        const data = sip[amt];
        if (!data) return;
        html += `<tr><td style="font-weight:600; white-space:nowrap;">${amt}</td>`;
        ['3Y', '5Y', '7Y', '10Y', '15Y', '20Y', '25Y'].forEach(years => {
            const d = data[years];
            if (d) {
                html += `<td>
                    <div style="font-weight:600; font-size:13px;">₹${d.future_value.toLocaleString('en-IN', {maximumFractionDigits:0})}</div>
                    <div style="font-size:10px; color:var(--text-muted);">Invested: ₹${d.total_invested.toLocaleString('en-IN', {maximumFractionDigits:0})}</div>
                    <div style="font-size:10px; color:var(--accent-green);">Profit: ₹${d.profit.toLocaleString('en-IN', {maximumFractionDigits:0})} (${d.multiplier}x)</div>
                </td>`;
            } else {
                html += '<td>—</td>';
            }
        });
        html += '</tr>';
    });

    html += '</tbody></table></div>';

    // Key insight
    const firstSip = sip['₹10,000/month'];
    if (firstSip && firstSip['20Y']) {
        const d = firstSip['20Y'];
        html += `
            <div style="margin-top:16px; padding:14px; background:rgba(6, 182, 212, 0.08); border:1px solid rgba(6, 182, 212, 0.2); border-radius:8px;">
                <div style="font-size:14px; font-weight:600; color:var(--accent-cyan);">💡 Key Insight</div>
                <div style="font-size:13px; color:var(--text-secondary); margin-top:4px;">
                    A ₹10,000/month SIP for 20 years = <strong>₹${d.total_invested.toLocaleString('en-IN', {maximumFractionDigits:0})}</strong> invested
                    → grows to <strong class="text-green">₹${d.future_value.toLocaleString('en-IN', {maximumFractionDigits:0})}</strong>
                    (Profit: <strong class="text-green">₹${d.profit.toLocaleString('en-IN', {maximumFractionDigits:0})}</strong>, ${d.multiplier}x return!)
                </div>
            </div>
        `;
    }

    html += '</div>';
    el.innerHTML = html;
}