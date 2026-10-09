// ================================================================
// FutureCandle — TradingView-Level Professional Frontend
// ================================================================

let activeSymbol = 'RELIANCE.NS';
let activeName = 'Reliance Industries';
let activeSector = 'Energy';
let allStocks = [];
let allIndices = [];
let allSymbols = [];
let sectors = [];
let tvChart = null;
let chartData = null;

// ---- INIT ----
document.addEventListener('DOMContentLoaded', async () => {
    await Promise.all([loadStocks(), loadIndices(), loadSectors(), loadCache()]);
    buildSidebar();
    buildTicker();
    setupGlobalSearch();
    // Auto-analyze default stock
    analyzeSymbol(activeSymbol);
});

// ---- DATA LOADING ----
async function loadStocks() {
    try { const r = await fetch('/api/stocks'); allStocks = await r.json(); } catch(e) { console.error(e); }
}

async function loadIndices() {
    try {
        const r = await fetch('/api/indices');
        const d = await r.json();
        allIndices = [];
        Object.values(d.categories || {}).forEach(cat => cat.forEach(i => allIndices.push(i)));
    } catch(e) { console.error(e); }
}

async function loadSectors() {
    try { const r = await fetch('/api/sectors'); sectors = await r.json(); } catch(e) { console.error(e); }
}

async function loadCache() {
    try {
        const r = await fetch('/api/cache/status');
        const d = await r.json();
        document.getElementById('cacheText').textContent = `${d.total_cached} symbols · refresh ${d.refresh_hours}h`;
    } catch(e) {
        document.getElementById('cacheText').textContent = 'Cache: loading...';
    }
}

// ---- SIDEBAR ----
function buildSidebar() {
    const container = document.getElementById('sectorList');
    document.getElementById('totalStockCount').textContent = `${allStocks.length} stocks + ${allIndices.length} indices`;

    let html = '';

    // Indices section
    html += `<div class="sector-group">
        <button class="sector-toggle" onclick="toggleSector(this)">
            <span>📈 Indices <span class="sector-count">(${allIndices.length})</span></span>
            <span class="arrow">▶</span>
        </button>
        <div class="sector-stocks" id="idxStocks">
            ${allIndices.map(i => `
                <div class="stock-item" onclick="selectAndAnalyze('${i.symbol}','${i.name}','${i.sector}','index')">
                    <span class="si-sym">${i.symbol.replace(/[\^\.].*/,'').substring(0,10)}</span>
                    <span class="si-name">${i.name}</span>
                </div>
            `).join('')}
        </div>
    </div>`;

    // Group stocks by sector
    const bySector = {};
    allStocks.forEach(s => {
        if (!bySector[s.sector]) bySector[s.sector] = [];
        bySector[s.sector].push(s);
    });

    Object.entries(bySector).sort((a,b) => b[1].length - a[1].length).forEach(([sector, stocks]) => {
        html += `<div class="sector-group">
            <button class="sector-toggle" onclick="toggleSector(this)">
                <span>${sector} <span class="sector-count">(${stocks.length})</span></span>
                <span class="arrow">▶</span>
            </button>
            <div class="sector-stocks">
                ${stocks.map(s => `
                    <div class="stock-item" onclick="selectAndAnalyze('${s.symbol}','${s.name}','${s.sector}','stock')">
                        <span class="si-sym">${s.symbol.replace('.NS','')}</span>
                        <span class="si-name">${s.name}</span>
                        <span class="si-cap">₹${(s.cap/100).toFixed(0)}K Cr</span>
                    </div>
                `).join('')}
            </div>
        </div>`;
    });

    container.innerHTML = html;
}

function toggleSector(btn) {
    btn.classList.toggle('open');
    const stocks = btn.nextElementSibling;
    stocks.classList.toggle('open');
}

// ---- TICKER ----
function buildTicker() {
    const keySyms = ['^NSEI','^BSESN','^CNXIT','^NSEBANK','NIFTY_PHARMA.NS','NIFTY_AUTO.NS',
        'NIFTY_FMCG.NS','NIFTY_METAL.NS','NIFTY_ENERGY.NS','NIFTY_REALTY.NS','NIFTY_DEFENCE.NS','^INDIAVIX'];
    const items = keySyms.map(sym => allIndices.find(i => i.symbol === sym)).filter(Boolean);
    // Duplicate for seamless scroll
    const doubled = [...items, ...items];
    document.getElementById('tickerTrack').innerHTML = doubled.map(i => {
        const cls = (i.change_pct||0) >= 0 ? 'up' : 'down';
        const sign = (i.change_pct||0) >= 0 ? '+' : '';
        return `<div class="tk" onclick="selectAndAnalyze('${i.symbol}','${i.name}','${i.sector}','index')">
            <span class="tk-name">${i.name}</span>
            <span class="tk-price">${i.price ? '₹'+i.price.toLocaleString('en-IN') : '—'}</span>
            <span class="tk-chg ${cls}">${sign}${(i.change_pct||0).toFixed(2)}%</span>
        </div>`;
    }).join('');
}

// ---- GLOBAL SEARCH ----
function setupGlobalSearch() {
    const input = document.getElementById('globalSearch');
    const dd = document.getElementById('searchDropdown');

    input.addEventListener('input', () => {
        const q = input.value.toLowerCase().trim();
        if (q.length < 1) { dd.classList.remove('show'); return; }

        // Search stocks
        const stockMatches = allStocks.filter(s =>
            s.symbol.toLowerCase().includes(q) || s.name.toLowerCase().includes(q) || s.sector.toLowerCase().includes(q)
        ).slice(0,8);

        // Search indices
        const idxMatches = allIndices.filter(i =>
            i.symbol.toLowerCase().includes(q) || i.name.toLowerCase().includes(q) || (i.sector||'').toLowerCase().includes(q)
        ).slice(0,5);

        // Quick: if user types a raw symbol like VEDL or FEDERALBNK
        const rawUpper = q.toUpperCase().replace(/[^A-Z0-9]/g,'');
        const dynamicEntry = (!stockMatches.find(s => s.symbol.startsWith(rawUpper)) && rawUpper.length >= 3)
            ? [{symbol: rawUpper + '.NS', name: rawUpper, sector: 'General', type: 'stock', cap: 50000}]
            : [];

        let html = '';
        if (idxMatches.length) {
            html += '<div class="sd-section">📈 Indices</div>';
            html += idxMatches.map(i => sdItem(i.symbol, i.name, i.sector, 'index', i.price)).join('');
        }
        if (stockMatches.length) {
            html += '<div class="sd-section">📊 Stocks</div>';
            html += stockMatches.map(s => sdItem(s.symbol, s.name, s.sector, 'stock')).join('');
        }
        if (dynamicEntry.length) {
            html += '<div class="sd-section">🔍 Try Symbol</div>';
            html += dynamicEntry.map(s => sdItem(s.symbol, s.name, s.sector, 'stock')).join('');
        }

        if (!html) html = '<div style="padding:16px;color:var(--text-3);text-align:center;">No results found</div>';
        dd.innerHTML = html;
        dd.classList.add('show');
    });

    input.addEventListener('focus', () => { if(input.value.length>0) input.dispatchEvent(new Event('input')); });
    document.addEventListener('click', e => { if(!e.target.closest('.nav-center')) dd.classList.remove('show'); });
    input.addEventListener('keydown', e => {
        if(e.key==='Enter') {
            const q = input.value.trim();
            if(q.length > 0) {
                const sym = q.includes('.') ? q.toUpperCase() : q.toUpperCase() + '.NS';
                selectAndAnalyze(sym, sym.replace('.NS',''), 'General', 'stock');
                dd.classList.remove('show');
                input.value = '';
            }
        }
    });
}

function sdItem(sym, name, sector, type, price) {
    const cleanSym = sym.replace('.NS','').replace('.BO','').replace('^','');
    return `<div class="sd-item" onclick="selectAndAnalyze('${sym}','${name}','${sector}','${type}')">
        <div class="sd-left">
            <span class="sd-sym">${cleanSym}</span>
            <span class="sd-name">${name}</span>
        </div>
        <div class="sd-right">
            ${price ? `<span class="sd-price">₹${price.toLocaleString('en-IN')}</span>` : ''}
            <span class="sd-badge ${type}">${type}</span>
        </div>
    </div>`;
}

// ---- SELECT & ANALYZE ----
function selectAndAnalyze(symbol, name, sector, type) {
    activeSymbol = symbol;
    activeName = name;
    activeSector = sector;
    document.getElementById('activeName').textContent = name;
    document.getElementById('activeSymbol').textContent = symbol.replace('.NS','').replace('.BO','').replace('^','');
    document.getElementById('activeSector').textContent = sector;
    document.getElementById('activeType').textContent = type || 'stock';
    document.getElementById('searchDropdown').classList.remove('show');
    document.getElementById('globalSearch').value = '';
    analyzeSymbol(symbol);
}

function analyzeActive() { analyzeSymbol(activeSymbol); }

async function analyzeSymbol(symbol) {
    const overlay = document.getElementById('loadingOverlay');
    document.getElementById('loadingSymbol').textContent = symbol;
    overlay.classList.remove('hidden');
    document.getElementById('analysisPanels').classList.add('hidden');

    try {
        const r = await fetch(`/api/analyze/${encodeURIComponent(symbol)}`);
        if (!r.ok) throw new Error('Analysis failed');
        const data = await r.json();

        // Update symbol bar
        document.getElementById('activeName').textContent = data.name;
        document.getElementById('activePrice').textContent = `₹${data.current_price.toLocaleString('en-IN',{minimumFractionDigits:2})}`;
        const sig = data.technical_analysis?.signal || {};
        const chgClass = (sig.score||50) >= 50 ? 'up' : 'down';
        document.getElementById('activeChange').textContent = `${sig.action||'N/A'} (${sig.score||0})`;
        document.getElementById('activeChange').className = `price-change ${chgClass}`;

        // Render chart
        chartData = data.chart_data;
        renderChart(chartData, 'line');

        // Render all panels
        renderSignal(data.technical_analysis, data.current_price);
        renderSentiment(data.sentiment);
        renderVerdict(data.investment, data.current_price);
        renderTech(data.technical_analysis);
        renderPatterns(data.candlestick_patterns);
        renderEntryExit(data.investment, data.current_price);
        renderInvest(data.investment);
        renderTargets(data.investment.price_targets, data.current_price);
        renderSIP(data.investment.sip);
        renderWealth(data.investment.projections);
        renderRisk(data.investment.risks);

        document.getElementById('analysisPanels').classList.remove('hidden');
    } catch(e) {
        console.error(e);
        alert('Analysis failed: ' + e.message);
    } finally {
        overlay.classList.add('hidden');
    }
}

// ---- CHART (Self-contained Canvas) ----
function renderChart(data, type) {
    const container = document.getElementById('tvChart');

    if (tvChart) { tvChart.destroy(); tvChart = null; }

    tvChart = new FCChart('tvChart');
    tvChart.type = type === 'candle' ? 'candle' : 'area';

    const dates = data.dates;
    const closes = data.closes;
    const opens = data.opens;
    const highs = data.highs;
    const lows = data.lows;

    if (type === 'candle') {
        const candleData = dates.map((d,i) => ({
            time: d, open: opens[i], high: highs[i], low: lows[i], close: closes[i]
        }));
        tvChart.setData(candleData);
    } else {
        const lineData = dates.map((d,i) => ({ time: d, value: closes[i] }));
        tvChart.setData(lineData);
    }

    // Add SMA overlays
    if (closes.length >= 20) {
        const sma20 = FCChart.computeSMA(dates.map((d,i) => ({time:d, value:closes[i]})), 20);
        tvChart.addOverlay(sma20, '#ffab00', 1, true);
    }
    if (closes.length >= 50) {
        const sma50 = FCChart.computeSMA(dates.map((d,i) => ({time:d, value:closes[i]})), 50);
        tvChart.addOverlay(sma50, '#ab47bc', 1, true);
    }

    document.getElementById('chartInfo').textContent = `${dates.length} candles · ${dates[0]} → ${dates[dates.length-1]}`;
}

function setTimeframe(btn, type) {
    document.querySelectorAll('.chart-tf').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    if (chartData) renderChart(chartData, type);
}

// ---- RENDER PANELS ----
function renderSignal(tech, price) {
    const sig = tech.signal;
    const score = sig.score;
    const color = score >= 60 ? 'var(--green)' : score >= 40 ? 'var(--yellow)' : 'var(--red)';
    const sr = tech.support_resistance || {};
    document.getElementById('pSignal').innerHTML = `
        <div class="signal-big" style="color:${color}">${sig.action.replace(/_/g,' ')}</div>
        <div class="signal-bar"><div class="signal-fill" style="width:${score}%;background:${color}"></div></div>
        <div style="text-align:center;font-size:12px;color:var(--text-3)">Score: ${score}/100 · Confidence: ${sig.confidence}%</div>
        <div class="signal-grid">
            <div class="signal-cell"><div class="sc-label">RSI</div><div class="sc-value">${tech.rsi?.value??'—'}</div></div>
            <div class="signal-cell"><div class="sc-label">MACD</div><div class="sc-value" style="font-size:11px">${(tech.macd?.signal_type||'—').replace(/_/g,' ')}</div></div>
            <div class="signal-cell"><div class="sc-label">Support</div><div class="sc-value" style="color:var(--green)">₹${(sr.nearest_support||0).toLocaleString('en-IN')}</div></div>
            <div class="signal-cell"><div class="sc-label">Resistance</div><div class="sc-value" style="color:var(--red)">₹${(sr.nearest_resistance||0).toLocaleString('en-IN')}</div></div>
        </div>`;
}

function renderSentiment(sent) {
    const fg = sent.fear_greed_index;
    document.getElementById('pSentiment').innerHTML = `
        <div class="sent-emoji">${sent.emoji}</div>
        <div class="sent-label">${sent.overall.replace(/_/g,' ')}</div>
        <div class="sent-score" style="color:${sent.composite_score>55?'var(--green)':sent.composite_score>40?'var(--yellow)':'var(--red)'}">${sent.composite_score}/100</div>
        <div class="fg-bar"><div class="fg-marker" style="left:${fg.index}%"></div></div>
        <div class="fg-labels"><span>Fear</span><span>Neutral</span><span>Greed</span></div>
        <div class="fg-zone">
            <div class="fgz">${fg.zone.replace(/_/g,' ')}</div>
            <div class="fgw">${fg.warning}</div>
        </div>`;
}

function renderVerdict(inv, price) {
    const v = inv.verdict;
    const stars = '★'.repeat(v.stars) + '☆'.repeat(5-v.stars);
    const color = v.stars>=4?'var(--green)':v.stars>=3?'var(--yellow)':'var(--red)';
    document.getElementById('pVerdict').innerHTML = `
        <div class="verdict-stars" style="color:${color}">${stars}</div>
        <div class="verdict-text" style="color:${color}">${v.verdict}</div>
        <div class="verdict-nums">
            <div class="vn"><div class="vn-label">CAGR</div><div class="vn-val" style="color:var(--cyan)">${v.expected_cagr}</div></div>
            <div class="vn"><div class="vn-label">5Y Target</div><div class="vn-val" style="color:var(--green)">${v.target_5_year}</div></div>
            <div class="vn"><div class="vn-label">10Y Target</div><div class="vn-val" style="color:var(--blue)">${v.target_10_year}</div></div>
            <div class="vn"><div class="vn-label">Duration</div><div class="vn-val">${inv.duration?.recommended||'N/A'}</div></div>
        </div>
        <div class="verdict-note">⏰ ${v.timing}</div>`;
}

function renderTech(tech) {
    const items = [];
    const add = (n,v,s,t) => items.push({n,v,s,t:t||'neut'});
    const rsi=tech.rsi||{}; add('RSI(14)',rsi.value,rsi.signal,rsi.value>50?'bull':'bear');
    const macd=tech.macd||{}; add('MACD',macd.histogram?.toFixed(3),(macd.signal_type||'').replace(/_/g,' '),macd.signal_type?.includes('BULL')?'bull':'bear');
    const stoch=tech.stochastic||{}; add('Stochastic',stoch.k,stoch.signal,stoch.k>50?'bull':'bear');
    const adx=tech.adx||{}; add('ADX',adx.value,`${adx.trend} ${adx.direction}`,adx.direction==='BULLISH'?'bull':'bear');
    const bb=tech.bollinger_bands||{}; add('Bollinger',`${bb.price_position}%`,bb.signal,bb.signal==='OVERSOLD'?'bull':bb.signal==='OVERBOUGHT'?'bear':'neut');
    const atr=tech.atr||{}; add('ATR',`₹${atr.value}`,'Vol: '+atr.volatility,'neut');
    const vwap=tech.vwap||{}; add('VWAP',`₹${vwap.value}`,vwap.signal,vwap.signal==='BULLISH'?'bull':'bear');
    const wr=tech.williams_r||{}; add('Williams %R',wr.value,wr.signal,wr.value>-50?'bull':'bear');
    const cci=tech.cci||{}; add('CCI',cci.value,cci.signal,cci.value>0?'bull':'bear');
    const mfi=tech.mfi||{}; add('MFI',mfi.value,mfi.signal,mfi.value>50?'bull':'bear');
    const roc=tech.roc||{}; add('ROC(12)',`${roc.value}%`,roc.signal,roc.value>0?'bull':'bear');
    const ichi=tech.ichimoku||{}; add('Ichimoku',(ichi.signal||'').replace(/_/g,' '),ichi.tk_cross,ichi.signal==='BULLISH'?'bull':ichi.signal==='BEARISH'?'bear':'neut');
    const st=tech.supertrend||{}; add('Supertrend',st.signal,st.signal,st.signal==='BULLISH'?'bull':st.signal==='BEARISH'?'bear':'neut');
    const ma=tech.moving_averages||{};
    if(ma.SMA_20) add('SMA 20',`₹${ma.SMA_20}`,ma.SMA_20_signal,ma.SMA_20_signal==='BULLISH'?'bull':'bear');
    if(ma.SMA_50) add('SMA 50',`₹${ma.SMA_50}`,ma.SMA_50_signal,ma.SMA_50_signal==='BULLISH'?'bull':'bear');
    if(ma.SMA_200) add('SMA 200',`₹${ma.SMA_200}`,ma.SMA_200_signal,ma.SMA_200_signal==='BULLISH'?'bull':'bear');
    if(ma.EMA_9) add('EMA 9',`₹${ma.EMA_9}`,ma.EMA_9_signal,ma.EMA_9_signal==='BULLISH'?'bull':'bear');
    if(ma.cross_signal) add('Cross',ma.cross_signal.replace(/_/g,' '),'',ma.cross_signal.includes('GOLDEN')?'bull':'bear');

    const scoreBadge = document.getElementById('techScoreBadge');
    const overall = tech.overall_score;
    scoreBadge.textContent = `${overall}/100`;
    scoreBadge.className = `panel-badge ${overall>=60?'bull':overall>=40?'neutral':'bear'}`;

    document.getElementById('pTech').innerHTML = `<div class="tech-grid">${items.map(i=>`
        <div class="tech-card ${i.t}">
            <div class="tc-name">${i.n}</div>
            <div class="tc-val">${i.v}</div>
            <div class="tc-sig" style="color:${i.t==='bull'?'var(--green)':i.t==='bear'?'var(--red)':'var(--yellow)'}">${i.s}</div>
        </div>`).join('')}</div>`;
}

function renderPatterns(data) {
    const recent = data.recent_patterns||[];
    const signal = data.signal||'NEUTRAL';
    const bull = data.bullish_score||50;
    const bear = data.bearish_score||50;

    const badge = document.getElementById('patternBadge');
    badge.textContent = `${data.total_patterns_detected} detected`;
    badge.className = `panel-badge ${signal==='BULLISH'?'bull':signal==='BEARISH'?'bear':'neutral'}`;

    let html = `<div style="display:flex;gap:8px;margin-bottom:12px">
        <div style="flex:${bull};height:6px;background:var(--green);border-radius:3px"></div>
        <div style="flex:${bear};height:6px;background:var(--red);border-radius:3px"></div>
    </div>
    <div style="display:flex;justify-content:space-between;font-size:11px;margin-bottom:12px">
        <span style="color:var(--green)">Bullish ${bull}%</span><span style="color:var(--red)">Bearish ${bear}%</span>
    </div>`;

    if (recent.length) {
        html += `<div class="pat-list">${recent.slice(-12).reverse().map(p=>{
            const icon = p.type==='bullish'?'🟢':'🔴';
            return `<div class="pat-row">
                <div class="pat-icon ${p.type==='bullish'?'bull':'bear'}">${icon}</div>
                <div class="pat-info"><div class="pat-name">${p.pattern.replace(/_/g,' ')}</div><div class="pat-date">${(p.date||'').split(' ')[0]} · ₹${(p.price||0).toLocaleString('en-IN')}</div></div>
                <span class="pat-str ${p.type==='bullish'?'bull':'bear'}">${p.type.toUpperCase()} ${(p.strength*100).toFixed(0)}%</span>
            </div>`;
        }).join('')}</div>`;
    }
    document.getElementById('pPatterns').innerHTML = html;
}

function renderEntryExit(inv, price) {
    const ee = inv.entry_exit || {};
    const stops = inv.duration || {};
    document.getElementById('pEntryExit').innerHTML = `
        <div style="margin-bottom:12px;font-size:12px;color:var(--text-2)">
            <strong>Current Price:</strong> <span style="font-family:var(--mono)">₹${price.toLocaleString('en-IN',{minimumFractionDigits:2})}</span>
        </div>
        <div class="ee-grid">
            <div class="ee-box buy"><div class="ee-label">🟢 Ideal Entry</div><div class="ee-val" style="color:var(--green)">₹${(ee.ideal_entry||0).toLocaleString('en-IN')}</div></div>
            <div class="ee-box buy"><div class="ee-label">🟢 Aggressive Entry</div><div class="ee-val" style="color:var(--green)">₹${(ee.aggressive_entry||0).toLocaleString('en-IN')}</div></div>
            <div class="ee-box buy"><div class="ee-label">🟢 Conservative Entry</div><div class="ee-val" style="color:var(--green)">₹${(ee.conservative_entry||0).toLocaleString('en-IN')}</div></div>
            <div class="ee-box buy"><div class="ee-label">🟢 Buy on Dip</div><div class="ee-val" style="color:var(--cyan)">₹${(ee.buy_on_dip||0).toLocaleString('en-IN')}</div></div>
            <div class="ee-box target"><div class="ee-label">🎯 Target 1</div><div class="ee-val" style="color:var(--blue)">₹${(ee.target_1||0).toLocaleString('en-IN')}</div></div>
            <div class="ee-box target"><div class="ee-label">🎯 Target 2</div><div class="ee-val" style="color:var(--blue)">₹${(ee.target_2||0).toLocaleString('en-IN')}</div></div>
            <div class="ee-box target"><div class="ee-label">🎯 Target 3</div><div class="ee-val" style="color:var(--blue)">₹${(ee.target_3||0).toLocaleString('en-IN')}</div></div>
            <div class="ee-box stop"><div class="ee-label">🛑 Stop Loss</div><div class="ee-val" style="color:var(--orange)">₹${(ee.stop_loss||0).toLocaleString('en-IN')} <span style="font-size:11px">(${ee.stop_loss_pct||0}%)</span></div></div>
        </div>
        <div style="margin-top:12px;padding:10px;background:var(--bg-2);border-radius:6px;font-size:12px;color:var(--text-2)">
            <strong>Risk/Reward Ratio:</strong> <span style="color:var(--yellow);font-weight:700">${ee.risk_reward_ratio||0}</span> ·
            <strong>Min Hold:</strong> ${stops.minimum||'N/A'} ·
            <strong>Recommended:</strong> <span style="color:var(--green)">${stops.recommended||'N/A'}</span> ·
            <strong>Optimal:</strong> ${stops.optimal||'N/A'}
        </div>
        <div style="margin-top:8px;padding:10px;background:var(--yellow-bg);border-radius:6px;font-size:11px;color:var(--yellow)">
            📋 ${stops.tax_note||''}
        </div>`;
}

function renderInvest(inv) {
    const s = inv.strategy || {};
    const a = inv.allocation || {};
    const alloc = a.asset_allocation || {};
    const cap = a.cap_allocation || {};
    const colors = {equity:'var(--blue)',debt:'var(--green)',gold:'var(--yellow)',cash:'var(--text-3)',
        large_cap:'var(--blue)',mid_cap:'var(--purple)',small_cap:'var(--orange)',micro_cap:'var(--red)'};

    let html = `
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px">
            <div style="padding:10px;background:var(--bg-2);border-radius:6px">
                <div style="font-size:10px;color:var(--text-3);text-transform:uppercase">Strategy</div>
                <div style="font-size:18px;font-weight:800;color:var(--blue);margin:4px 0">${(s.type||'').replace(/_/g,' ')}</div>
                <div style="font-size:11px;color:var(--text-2)">${s.description||''}</div>
            </div>
            <div style="padding:10px;background:var(--bg-2);border-radius:6px">
                <div style="font-size:10px;color:var(--text-3);text-transform:uppercase">Investment Mode</div>
                <div style="font-size:14px;font-weight:700;color:var(--purple);margin:4px 0">${s.investment_mode||''}</div>
                <div style="font-size:11px;color:var(--text-2)">${s.mode_reason||''}</div>
            </div>
        </div>
        <div style="font-size:12px;font-weight:700;margin-bottom:8px;color:var(--text-2)">💼 Asset Allocation</div>`;

    ['equity','debt','gold','cash'].forEach(k => {
        if(alloc[k]!==undefined) html += allocBar(k, alloc[k], colors[k]);
    });

    html += `<div style="font-size:12px;font-weight:700;margin:16px 0 8px;color:var(--text-2)">📐 Market Cap Allocation</div>`;
    ['large_cap','mid_cap','small_cap','micro_cap'].forEach(k => {
        if(cap[k]!==undefined) html += allocBar(k.replace(/_/g,' '), cap[k], colors[k]);
    });

    if (a.sector_suggestions) {
        html += `<div style="font-size:12px;font-weight:700;margin:16px 0 8px;color:var(--text-2)">🏭 Sector Focus</div>
        <div class="sector-tags">${a.sector_suggestions.map(s=>`<span class="stag"><span class="stw">${s.weight}%</span> ${s.sector}</span>`).join('')}</div>`;
    }

    document.getElementById('pInvest').innerHTML = html;
}

function allocBar(label, pct, color) {
    return `<div class="alloc-row">
        <div class="alloc-hdr"><span>${label}</span><span style="font-weight:700;color:${color}">${pct}%</span></div>
        <div class="alloc-bar"><div class="alloc-fill" style="width:${pct}%;background:${color}"></div></div>
    </div>`;
}

function renderTargets(targets, price) {
    const scenarios = ['conservative','moderate','aggressive'];
    const tfs = ['1Y','3Y','5Y','7Y','10Y','15Y','20Y'];
    const colors = {conservative:'var(--green)',moderate:'var(--blue)',aggressive:'var(--yellow)'};

    let html = `<div style="overflow-x:auto"><table class="fc-table"><thead><tr><th>Scenario</th>${tfs.map(t=>`<th>${t}</th>`).join('')}</tr></thead><tbody>`;
    scenarios.forEach(sc => {
        const s = targets[sc]||{};
        html += `<tr><td style="font-weight:700;color:${colors[sc]}">${sc.toUpperCase()}</td>`;
        tfs.forEach(tf => {
            const d = s[tf];
            html += d ? `<td><div style="font-weight:700">₹${d.price?.toLocaleString('en-IN',{maximumFractionDigits:0})}</div><div style="font-size:10px;color:var(--green)">+${d.return_pct}% (${d.cagr}%)</div></td>` : '<td>—</td>';
        });
        html += '</tr>';
    });
    html += '</tbody></table></div>';

    const nt = targets.near_term||{};
    html += `<div style="margin-top:16px;font-size:12px;font-weight:700;color:var(--text-2);margin-bottom:8px">📅 Near-Term Targets</div>
    <div class="ee-grid">
        <div class="ee-box target"><div class="ee-label">3M Bull</div><div class="ee-val" style="color:var(--green)">₹${(nt['3_month_bull']||0).toLocaleString('en-IN',{maximumFractionDigits:0})}</div></div>
        <div class="ee-box stop"><div class="ee-label">3M Bear</div><div class="ee-val" style="color:var(--red)">₹${(nt['3_month_bear']||0).toLocaleString('en-IN',{maximumFractionDigits:0})}</div></div>
        <div class="ee-box target"><div class="ee-label">6M Bull</div><div class="ee-val" style="color:var(--green)">₹${(nt['6_month_bull']||0).toLocaleString('en-IN',{maximumFractionDigits:0})}</div></div>
        <div class="ee-box stop"><div class="ee-label">6M Bear</div><div class="ee-val" style="color:var(--red)">₹${(nt['6_month_bear']||0).toLocaleString('en-IN',{maximumFractionDigits:0})}</div></div>
        <div class="ee-box target"><div class="ee-label">1Y Bull</div><div class="ee-val" style="color:var(--green)">₹${(nt['1_year_bull']||0).toLocaleString('en-IN',{maximumFractionDigits:0})}</div></div>
        <div class="ee-box stop"><div class="ee-label">1Y Bear</div><div class="ee-val" style="color:var(--red)">₹${(nt['1_year_bear']||0).toLocaleString('en-IN',{maximumFractionDigits:0})}</div></div>
    </div>`;
    document.getElementById('pTargets').innerHTML = html;
}

function renderSIP(sip) {
    const s = sip||{};
    document.getElementById('pSIP').innerHTML = `
        <div style="padding:12px;background:var(--bg-2);border-radius:6px;border-left:3px solid var(--cyan)">
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:12px">
                <div><span style="color:var(--text-3)">Frequency:</span> ${s.recommended_frequency}</div>
                <div><span style="color:var(--text-3)">Income %:</span> <span style="color:var(--green);font-weight:700">${s.income_allocation_pct}%</span></div>
                <div><span style="color:var(--text-3)">Duration:</span> ${s.duration}</div>
                <div><span style="color:var(--text-3)">Best Day:</span> ${s.best_day}</div>
                <div><span style="color:var(--text-3)">Min:</span> ${s.minimum_investment}</div>
                <div><span style="color:var(--text-3)">Auto:</span> ${s.auto_invest}</div>
            </div>
            ${s.step_up?.note ? `<div style="margin-top:8px;font-size:11px;color:var(--text-2)">💡 ${s.step_up.note}</div>` : ''}
            ${s.platforms ? `<div style="margin-top:8px;font-size:10px;color:var(--text-3)">Platforms: ${s.platforms.join(' · ')}</div>` : ''}
        </div>`;
}

function renderWealth(proj) {
    if(!proj) { document.getElementById('pWealth').innerHTML=''; return; }
    const sip = proj.sip||{};
    const showSips = ['₹5,000/month','₹10,000/month','₹25,000/month','₹50,000/month'];
    const yrs = ['5Y','10Y','15Y','20Y'];

    let html = `<div style="font-size:12px;font-weight:700;color:var(--text-2);margin-bottom:8px">📈 Monthly SIP Growth</div>
    <div style="overflow-x:auto"><table class="fc-table"><thead><tr><th>SIP</th>${yrs.map(y=>`<th>${y}</th>`).join('')}</tr></thead><tbody>`;
    showSips.forEach(amt => {
        const d = sip[amt];
        if(!d) return;
        html += `<tr><td style="font-weight:700">${amt}</td>`;
        yrs.forEach(y => {
            const v = d[y];
            html += v ? `<td><div style="font-weight:700">₹${v.future_value.toLocaleString('en-IN',{maximumFractionDigits:0})}</div><div style="font-size:10px;color:var(--green)">+${v.multiplier}x · Profit ₹${v.profit.toLocaleString('en-IN',{maximumFractionDigits:0})}</div></td>` : '<td>—</td>';
        });
        html += '</tr>';
    });
    html += '</tbody></table></div>';

    // Key insight
    const d10 = sip['₹10,000/month']?.['20Y'];
    if(d10) {
        html += `<div style="margin-top:12px;padding:10px;background:var(--cyan-bg);border:1px solid rgba(0,188,212,.2);border-radius:6px;font-size:12px">
            💡 <strong>₹10K/month for 20Y:</strong> Invest <strong>₹${d10.total_invested.toLocaleString('en-IN',{maximumFractionDigits:0})}</strong> → grows to <strong style="color:var(--green)">₹${d10.future_value.toLocaleString('en-IN',{maximumFractionDigits:0})}</strong> (${d10.multiplier}x)
        </div>`;
    }
    document.getElementById('pWealth').innerHTML = html;
}

function renderRisk(risks) {
    const items = risks.individual_risks||[];
    const overall = risks.overall_risk_level||'UNKNOWN';
    const counts = risks.risk_count||{};

    let html = `<div style="display:flex;gap:12px;align-items:center;margin-bottom:12px;padding:10px;background:var(--bg-2);border-radius:6px">
        <span style="font-size:13px;color:var(--text-3)">Overall Risk:</span>
        <span style="font-size:18px;font-weight:800" class="risk-badge ${overall.toLowerCase().replace('_','-')}">${overall.replace(/_/g,' ')}</span>
        <span style="font-size:11px;color:var(--text-3)">(${counts.high||0} High · ${counts.medium||0} Med · ${counts.low||0} Low)</span>
    </div>`;

    items.forEach(r => {
        const lvl = r.level.toLowerCase();
        html += `<div class="risk-row ${lvl}">
            <span class="risk-badge ${lvl}">${r.level}</span>
            <div><div class="risk-type">${r.type}</div><div class="risk-detail">${r.detail}</div></div>
        </div>`;
    });

    document.getElementById('pRisk').innerHTML = html;
}