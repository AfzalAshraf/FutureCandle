// ================================================================
// FutureCandle — App JS (Modern Fintech)
// ================================================================

let activeSymbol = 'RELIANCE.NS';
let activeName = 'Reliance Industries';
let activeSector = 'Energy';
let allStocks = [];
let allIndices = [];
let sectors = [];
let browseMode = 'stocks';
let fcChart = null;
let chartData = null;

document.addEventListener('DOMContentLoaded', async () => {
    await Promise.all([loadStocks(), loadIndices(), loadSectors(), loadCache()]);
    buildTicker();
    buildBrowse();
    setupSearch();
    selectAndAnalyze('RELIANCE.NS', 'Reliance Industries', 'Energy', 'stock');
});

// ---- DATA ----
async function loadStocks() { try { const r = await fetch('/api/stocks'); allStocks = await r.json(); } catch(e){} }
async function loadIndices() {
    try {
        const r = await fetch('/api/indices'); const d = await r.json();
        allIndices = []; Object.values(d.categories||{}).forEach(c => c.forEach(i => allIndices.push(i)));
    } catch(e){}
}
async function loadSectors() { try { const r = await fetch('/api/sectors'); sectors = await r.json(); } catch(e){} }
async function loadCache() {
    try {
        const r = await fetch('/api/cache/status'); const d = await r.json();
        document.getElementById('cacheBadge').textContent = `${d.total_cached} symbols · ${d.refresh_hours}h refresh`;
    } catch(e){}
}

// ---- TICKER ----
function buildTicker() {
    const keys = ['^NSEI','^BSESN','^CNXIT','^NSEBANK','NIFTY_PHARMA.NS','NIFTY_AUTO.NS','NIFTY_FMCG.NS','NIFTY_METAL.NS','NIFTY_ENERGY.NS','NIFTY_REALTY.NS','NIFTY_DEFENCE.NS','^INDIAVIX'];
    const items = keys.map(s => allIndices.find(i=>i.symbol===s)).filter(Boolean);
    const doubled = [...items, ...items];
    document.getElementById('tickerTrack').innerHTML = doubled.map(i => {
        const cls = (i.change_pct||0)>=0?'up':'dn';
        const sign = (i.change_pct||0)>=0?'+':'';
        return `<div class="tk" onclick="selectAndAnalyze('${i.symbol}','${i.name}','${i.sector}','index')">
            <span class="tk-n">${i.name}</span>
            <span class="tk-p">${i.price?'₹'+i.price.toLocaleString('en-IN'):'—'}</span>
            <span class="tk-c ${cls}">${sign}${(i.change_pct||0).toFixed(2)}%</span>
        </div>`;
    }).join('');
}

// ---- BROWSE ----
function buildBrowse(mode) {
    if(mode) browseMode = mode;
    document.getElementById('stockCountBadge').textContent = `(${allStocks.length})`;
    const list = document.getElementById('browseList');
    const q = (document.getElementById('browseSearch').value||'').toLowerCase();

    let html = '';
    if(browseMode === 'stocks') {
        const filtered = allStocks.filter(s => !q || s.symbol.toLowerCase().includes(q) || s.name.toLowerCase().includes(q) || s.sector.toLowerCase().includes(q));
        html = filtered.slice(0,200).map(s =>
            `<div class="brow-item" onclick="selectAndAnalyze('${s.symbol}','${s.name}','${s.sector}','stock')">
                <span class="bi-sym">${s.symbol.replace('.NS','')}</span>
                <span class="bi-name">${s.name}</span>
                <span class="bi-r">${s.sector}</span>
            </div>`
        ).join('');
    } else if(browseMode === 'indices') {
        const filtered = allIndices.filter(i => !q || i.name.toLowerCase().includes(q) || i.symbol.toLowerCase().includes(q));
        html = filtered.map(i =>
            `<div class="brow-item" onclick="selectAndAnalyze('${i.symbol}','${i.name}','${i.sector}','index')">
                <span class="bi-sym">${i.symbol.replace(/[\^\.].*/,'').substring(0,10)}</span>
                <span class="bi-name">${i.name}</span>
                <span class="bi-r">${i.exchange||''}</span>
            </div>`
        ).join('');
    } else {
        // sectors view
        const bySec = {};
        allStocks.forEach(s => { if(!bySec[s.sector]) bySec[s.sector]=[]; bySec[s.sector].push(s); });
        Object.entries(bySec).sort((a,b)=>b[1].length-a[1].length).forEach(([sec,stocks]) => {
            if(q && !sec.toLowerCase().includes(q)) return;
            html += `<div style="padding:8px 12px;font-size:11px;font-weight:700;color:var(--green);background:var(--bg3);border-bottom:1px solid var(--border)">${sec} (${stocks.length})</div>`;
            stocks.filter(s => !q || s.name.toLowerCase().includes(q) || s.symbol.toLowerCase().includes(q)).slice(0,30).forEach(s => {
                html += `<div class="brow-item" onclick="selectAndAnalyze('${s.symbol}','${s.name}','${s.sector}','stock')">
                    <span class="bi-sym">${s.symbol.replace('.NS','')}</span>
                    <span class="bi-name">${s.name}</span>
                    <span class="bi-r">${s.sector}</span>
                </div>`;
            });
        });
    }
    list.innerHTML = html || '<div style="padding:20px;text-align:center;color:var(--text3)">No results</div>';
}

function browseTab(btn, mode) {
    document.querySelectorAll('.btab').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    buildBrowse(mode);
}

function filterBrowse(q) { buildBrowse(); }

// ---- GLOBAL SEARCH ----
function setupSearch() {
    const input = document.getElementById('globalSearch');
    const dd = document.getElementById('searchDD');

    input.addEventListener('input', () => {
        const q = input.value.toLowerCase().trim();
        if(q.length<1){dd.classList.remove('show');return}

        const sMatch = allStocks.filter(s => s.symbol.toLowerCase().includes(q)||s.name.toLowerCase().includes(q)||s.sector.toLowerCase().includes(q)).slice(0,8);
        const iMatch = allIndices.filter(i => i.symbol.toLowerCase().includes(q)||i.name.toLowerCase().includes(q)).slice(0,5);

        const rawUpper = q.toUpperCase().replace(/[^A-Z0-9]/g,'');
        const dyn = (!sMatch.find(s=>s.symbol.startsWith(rawUpper)) && rawUpper.length>=3)
            ? [{symbol:rawUpper+'.NS',name:rawUpper,sector:'General',type:'stock'}] : [];

        let html = '';
        if(iMatch.length){html+='<div class="sd-section">📈 Indices</div>'+iMatch.map(i=>sdItem(i.symbol,i.name,i.sector,'index',i.price)).join('')}
        if(sMatch.length){html+='<div class="sd-section">📊 Stocks</div>'+sMatch.map(s=>sdItem(s.symbol,s.name,s.sector,'stock')).join('')}
        if(dyn.length){html+='<div class="sd-section">🔍 Try Symbol</div>'+dyn.map(s=>sdItem(s.symbol,s.name,s.sector,'stock')).join('')}
        if(!html) html='<div style="padding:16px;color:var(--text3);text-align:center">No results</div>';
        dd.innerHTML=html;dd.classList.add('show');
    });

    input.addEventListener('focus',()=>{if(input.value.length>0)input.dispatchEvent(new Event('input'))});
    document.addEventListener('click',e=>{if(!e.target.closest('.nav-search'))dd.classList.remove('show')});
    input.addEventListener('keydown',e=>{
        if(e.key==='Enter'){const q=input.value.trim();if(q.length>0){const sym=q.includes('.')?q.toUpperCase():q.toUpperCase()+'.NS';selectAndAnalyze(sym,sym.replace('.NS',''),'General','stock');dd.classList.remove('show');input.value=''}}
    });
}

function sdItem(sym,name,sector,type,price){
    const clean=sym.replace('.NS','').replace('.BO','').replace('^','');
    return `<div class="sd-item" onclick="selectAndAnalyze('${sym}','${name}','${sector}','${type}')">
        <div class="sd-left"><span class="sd-sym">${clean}</span><span class="sd-name">${name}</span></div>
        <div>${price?'<span class="sd-price">₹'+price.toLocaleString('en-IN')+'</span>':''} <span class="sd-badge ${type}">${type}</span></div>
    </div>`;
}

// ---- SELECT & ANALYZE ----
function selectAndAnalyze(sym,name,sector,type){
    activeSymbol=sym;activeName=name;activeSector=sector;
    document.getElementById('aName').textContent=name;
    document.getElementById('aSym').textContent=sym.replace('.NS','').replace('.BO','').replace('^','');
    document.getElementById('aSector').textContent=sector;
    document.getElementById('searchDD').classList.remove('show');
    document.getElementById('globalSearch').value='';
    doAnalyze(sym);
}

function analyzeActive(){doAnalyze(activeSymbol)}

async function doAnalyze(symbol){
    document.getElementById('loadSym').textContent=symbol;
    document.getElementById('loader').classList.remove('hidden');
    document.getElementById('results').classList.add('hidden');

    try{
        const r=await fetch(`/api/analyze/${encodeURIComponent(symbol)}`);
        if(!r.ok)throw new Error('Failed');
        const d=await r.json();

        // Price
        document.getElementById('aPrice').textContent=`₹${d.current_price.toLocaleString('en-IN',{minimumFractionDigits:2})}`;
        const sig=d.technical_analysis?.signal||{};
        const cls=(sig.score||50)>=50?'up':'dn';
        document.getElementById('aChange').textContent=`${sig.action||'N/A'} (${sig.score||0})`;
        document.getElementById('aChange').className=`sh-change ${cls}`;

        // Chart
        chartData=d.chart_data;renderChart(chartData,'area');

        // Panels
        renderSignal(d.technical_analysis,d.current_price);
        renderSentiment(d.sentiment);
        renderVerdict(d.investment,d.current_price);
        renderEntryExit(d.investment,d.current_price);
        renderInvest(d.investment);
        renderTech(d.technical_analysis);
        renderPatterns(d.candlestick_patterns);
        renderTargets(d.investment.price_targets,d.current_price);
        renderSIP(d.investment.sip);
        renderWealth(d.investment.projections);
        renderRisk(d.investment.risks);

        document.getElementById('results').classList.remove('hidden');
    }catch(e){alert('Error: '+e.message)}
    finally{document.getElementById('loader').classList.add('hidden')}
}

// ---- CHART ----
function renderChart(data,type){
    if(fcChart){fcChart.destroy();fcChart=null}
    fcChart=new FCChart('chartContainer');
    fcChart.type=type==='candle'?'candle':'area';

    const dates=data.dates,closes=data.closes,opens=data.opens,highs=data.highs,lows=data.lows;
    if(type==='candle'){
        fcChart.setData(dates.map((d,i)=>({time:d,open:opens[i],high:highs[i],low:lows[i],close:closes[i]})));
    }else{
        fcChart.setData(dates.map((d,i)=>({time:d,value:closes[i]})));
    }
    if(closes.length>=20){
        const sma=FCChart.computeSMA(dates.map((d,i)=>({time:d,value:closes[i]})),20);
        fcChart.addOverlay(sma,'#ffab00',1,true);
    }
    if(closes.length>=50){
        const sma=FCChart.computeSMA(dates.map((d,i)=>({time:d,value:closes[i]})),50);
        fcChart.addOverlay(sma,'#a55eea',1,true);
    }
    document.getElementById('chartLabel').textContent=`${dates.length} candles · ${dates[0]} → ${dates[dates.length-1]}`;
}

function setCType(btn,type){
    document.querySelectorAll('.cbtn').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    if(chartData)renderChart(chartData,type);
}

// ---- RENDER PANELS ----
function renderSignal(tech,price){
    const sig=tech.signal,score=sig.score;
    const color=score>=60?'var(--green)':score>=40?'var(--yellow)':'var(--red)';
    const sr=tech.support_resistance||{};
    document.getElementById('rSignal').innerHTML=`
        <div class="sig-big" style="color:${color}">${sig.action.replace(/_/g,' ')}</div>
        <div class="sig-bar"><div class="sig-fill" style="width:${score}%;background:${color}"></div></div>
        <div style="text-align:center;font-size:11px;color:var(--text3)">Score: ${score}/100 · Confidence: ${sig.confidence}%</div>
        <div class="sig-row">
            <div class="sig-cell"><div class="sig-l">RSI</div><div class="sig-v">${tech.rsi?.value??'—'}</div></div>
            <div class="sig-cell"><div class="sig-l">MACD</div><div class="sig-v" style="font-size:11px">${(tech.macd?.signal_type||'—').replace(/_/g,' ')}</div></div>
            <div class="sig-cell"><div class="sig-l">Support</div><div class="sig-v" style="color:var(--green)">₹${(sr.nearest_support||0).toLocaleString('en-IN')}</div></div>
            <div class="sig-cell"><div class="sig-l">Resistance</div><div class="sig-v" style="color:var(--red)">₹${(sr.nearest_resistance||0).toLocaleString('en-IN')}</div></div>
        </div>`;
}

function renderSentiment(sent){
    const fg=sent.fear_greed_index;
    document.getElementById('rSentiment').innerHTML=`
        <div class="s-emoji">${sent.emoji}</div>
        <div class="s-lbl">${sent.overall.replace(/_/g,' ')}</div>
        <div class="s-score" style="color:${sent.composite_score>55?'var(--green)':sent.composite_score>40?'var(--yellow)':'var(--red)'}">${sent.composite_score}/100</div>
        <div class="fg-bar"><div class="fg-dot" style="left:${fg.index}%"></div></div>
        <div class="fg-labels"><span>Fear</span><span>Neutral</span><span>Greed</span></div>
        <div class="fg-box"><div class="fg-zone">${fg.zone.replace(/_/g,' ')}</div><div class="fg-warn">${fg.warning}</div></div>`;
}

function renderVerdict(inv,price){
    const v=inv.verdict,stars='★'.repeat(v.stars)+'☆'.repeat(5-v.stars);
    const color=v.stars>=4?'var(--green)':v.stars>=3?'var(--yellow)':'var(--red)';
    document.getElementById('rVerdict').innerHTML=`
        <div class="v-stars" style="color:${color}">${stars}</div>
        <div class="v-text" style="color:${color}">${v.verdict}</div>
        <div class="v-nums">
            <div class="vn"><div class="vn-l">CAGR</div><div class="vn-v" style="color:var(--cyan)">${v.expected_cagr}</div></div>
            <div class="vn"><div class="vn-l">5Y Target</div><div class="vn-v" style="color:var(--green)">${v.target_5_year}</div></div>
            <div class="vn"><div class="vn-l">10Y Target</div><div class="vn-v" style="color:var(--blue)">${v.target_10_year}</div></div>
            <div class="vn"><div class="vn-l">Duration</div><div class="vn-v">${inv.duration?.recommended||'N/A'}</div></div>
        </div>
        <div class="v-note">⏰ ${v.timing}</div>`;
}

function renderEntryExit(inv,price){
    const ee=inv.entry_exit||{},dur=inv.duration||{};
    document.getElementById('rEntryExit').innerHTML=`
        <div style="font-size:12px;color:var(--text2);margin-bottom:10px">Current Price: <strong style="font-family:monospace">₹${price.toLocaleString('en-IN',{minimumFractionDigits:2})}</strong></div>
        <div class="ee-grid">
            <div class="ee-box buy"><div class="ee-l">🟢 Ideal Entry</div><div class="ee-v" style="color:var(--green)">₹${(ee.ideal_entry||0).toLocaleString('en-IN')}</div></div>
            <div class="ee-box buy"><div class="ee-l">🟢 Buy on Dip</div><div class="ee-v" style="color:var(--cyan)">₹${(ee.buy_on_dip||0).toLocaleString('en-IN')}</div></div>
            <div class="ee-box target"><div class="ee-l">🎯 Target 1</div><div class="ee-v" style="color:var(--blue)">₹${(ee.target_1||0).toLocaleString('en-IN')}</div></div>
            <div class="ee-box target"><div class="ee-l">🎯 Target 2</div><div class="ee-v" style="color:var(--blue)">₹${(ee.target_2||0).toLocaleString('en-IN')}</div></div>
            <div class="ee-box target"><div class="ee-l">🎯 Target 3</div><div class="ee-v" style="color:var(--blue)">₹${(ee.target_3||0).toLocaleString('en-IN')}</div></div>
            <div class="ee-box stop"><div class="ee-l">🛑 Stop Loss</div><div class="ee-v" style="color:var(--orange)">₹${(ee.stop_loss||0).toLocaleString('en-IN')} <small>(${ee.stop_loss_pct||0}%)</small></div></div>
        </div>
        <div class="ee-info">
            <strong>Risk/Reward:</strong> <span style="color:var(--yellow);font-weight:700">${ee.risk_reward_ratio||0}</span> ·
            <strong>Min Hold:</strong> ${dur.minimum||'N/A'} ·
            <strong>Recommended:</strong> <span style="color:var(--green)">${dur.recommended||'N/A'}</span> ·
            <strong>Optimal:</strong> ${dur.optimal||'N/A'}
        </div>
        <div style="margin-top:8px;padding:8px;background:var(--yellow-bg);border-radius:8px;font-size:11px;color:var(--yellow)">📋 ${dur.tax_note||''}</div>`;
}

function renderInvest(inv){
    const s=inv.strategy||{},a=inv.allocation||{},alloc=a.asset_allocation||{},cap=a.cap_allocation||{};
    const colors={equity:'var(--blue)',debt:'var(--green)',gold:'var(--yellow)',cash:'var(--text3)',large_cap:'var(--blue)',mid_cap:'var(--purple)',small_cap:'var(--orange)',micro_cap:'var(--red)'};
    let html=`<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px">
        <div style="padding:10px;background:var(--bg);border-radius:8px"><div style="font-size:10px;color:var(--text3);text-transform:uppercase">Strategy</div><div style="font-size:16px;font-weight:800;color:var(--blue);margin:4px 0">${(s.type||'').replace(/_/g,' ')}</div><div style="font-size:11px;color:var(--text2)">${s.description||''}</div></div>
        <div style="padding:10px;background:var(--bg);border-radius:8px"><div style="font-size:10px;color:var(--text3);text-transform:uppercase">Mode</div><div style="font-size:13px;font-weight:700;color:var(--purple);margin:4px 0">${s.investment_mode||''}</div><div style="font-size:11px;color:var(--text2)">${s.mode_reason||''}</div></div>
    </div>`;
    ['equity','debt','gold','cash'].forEach(k=>{if(alloc[k]!==undefined)html+=allocBar(k,alloc[k],colors[k])});
    html+=`<div style="font-size:11px;font-weight:700;margin:14px 0 6px;color:var(--text3)">📐 Cap Allocation</div>`;
    ['large_cap','mid_cap','small_cap','micro_cap'].forEach(k=>{if(cap[k]!==undefined)html+=allocBar(k.replace(/_/g,' '),cap[k],colors[k])});
    if(a.sector_suggestions)html+=`<div style="font-size:11px;font-weight:700;margin:14px 0 6px;color:var(--text3)">🏭 Sector Focus</div><div class="stags">${a.sector_suggestions.map(s=>`<span class="stag"><b>${s.weight}%</b> ${s.sector}</span>`).join('')}</div>`;
    document.getElementById('rInvest').innerHTML=html;
}

function allocBar(l,p,c){return`<div class="alloc"><div class="alloc-h"><span>${l}</span><span style="font-weight:700;color:${c}">${p}%</span></div><div class="alloc-b"><div class="alloc-f" style="width:${p}%;background:${c}"></div></div></div>`}

function renderTech(tech){
    const items=[];
    const add=(n,v,s,t)=>items.push({n,v,s,t:t||'neut'});
    const rsi=tech.rsi||{};add('RSI(14)',rsi.value,rsi.signal,rsi.value>50?'bull':'bear');
    const macd=tech.macd||{};add('MACD',macd.histogram?.toFixed(3),(macd.signal_type||'').replace(/_/g,' '),macd.signal_type?.includes('BULL')?'bull':'bear');
    const stoch=tech.stochastic||{};add('Stochastic',stoch.k,stoch.signal,stoch.k>50?'bull':'bear');
    const adx=tech.adx||{};add('ADX',adx.value,`${adx.trend} ${adx.direction}`,adx.direction==='BULLISH'?'bull':'bear');
    const bb=tech.bollinger_bands||{};add('Bollinger',`${bb.price_position}%`,bb.signal,bb.signal==='OVERSOLD'?'bull':bb.signal==='OVERBOUGHT'?'bear':'neut');
    const atr=tech.atr||{};add('ATR',`₹${atr.value}`,'Vol: '+atr.volatility,'neut');
    const vwap=tech.vwap||{};add('VWAP',`₹${vwap.value}`,vwap.signal,vwap.signal==='BULLISH'?'bull':'bear');
    const wr=tech.williams_r||{};add('Williams %R',wr.value,wr.signal,wr.value>-50?'bull':'bear');
    const cci=tech.cci||{};add('CCI',cci.value,cci.signal,cci.value>0?'bull':'bear');
    const mfi=tech.mfi||{};add('MFI',mfi.value,mfi.signal,mfi.value>50?'bull':'bear');
    const roc=tech.roc||{};add('ROC(12)',`${roc.value}%`,roc.signal,roc.value>0?'bull':'bear');
    const ichi=tech.ichimoku||{};add('Ichimoku',(ichi.signal||'').replace(/_/g,' '),ichi.tk_cross,ichi.signal==='BULLISH'?'bull':ichi.signal==='BEARISH'?'bear':'neut');
    const st=tech.supertrend||{};add('Supertrend',st.signal,st.signal,st.signal==='BULLISH'?'bull':st.signal==='BEARISH'?'bear':'neut');
    const ma=tech.moving_averages||{};
    if(ma.SMA_20)add('SMA 20',`₹${ma.SMA_20}`,ma.SMA_20_signal,ma.SMA_20_signal==='BULLISH'?'bull':'bear');
    if(ma.SMA_50)add('SMA 50',`₹${ma.SMA_50}`,ma.SMA_50_signal,ma.SMA_50_signal==='BULLISH'?'bull':'bear');
    if(ma.SMA_200)add('SMA 200',`₹${ma.SMA_200}`,ma.SMA_200_signal,ma.SMA_200_signal==='BULLISH'?'bull':'bear');
    if(ma.EMA_9)add('EMA 9',`₹${ma.EMA_9}`,ma.EMA_9_signal,ma.EMA_9_signal==='BULLISH'?'bull':'bear');
    if(ma.cross_signal)add('Cross',ma.cross_signal.replace(/_/g,' '),'',ma.cross_signal.includes('GOLDEN')?'bull':'bear');
    const ob=tech.overall_score;const tb=document.getElementById('techBadge');tb.textContent=`${ob}/100`;tb.className=`card-badge ${ob>=60?'bull':ob>=40?'neut':'bear'}`;
    document.getElementById('rTech').innerHTML=`<div class="tech-grid">${items.map(i=>`<div class="tc ${i.t}"><div class="tc-n">${i.n}</div><div class="tc-v">${i.v}</div><div class="tc-s" style="color:${i.t==='bull'?'var(--green)':i.t==='bear'?'var(--red)':'var(--yellow)'}">${i.s}</div></div>`).join('')}</div>`;
}

function renderPatterns(data){
    const recent=data.recent_patterns||[],signal=data.signal||'NEUTRAL',bull=data.bullish_score||50,bear=data.bearish_score||50;
    const pb=document.getElementById('patBadge');pb.textContent=`${data.total_patterns_detected} detected`;pb.className=`card-badge ${signal==='BULLISH'?'bull':signal==='BEARISH'?'bear':'neut'}`;
    let html=`<div style="display:flex;gap:6px;margin-bottom:10px"><div style="flex:${bull};height:5px;background:var(--green);border-radius:3px"></div><div style="flex:${bear};height:5px;background:var(--red);border-radius:3px"></div></div><div style="display:flex;justify-content:space-between;font-size:10px;margin-bottom:10px"><span style="color:var(--green)">Bullish ${bull}%</span><span style="color:var(--red)">Bearish ${bear}%</span></div>`;
    if(recent.length)html+=`<div class="pat-list">${recent.slice(-10).reverse().map(p=>`<div class="pat"><div class="pat-i ${p.type==='bullish'?'bull':'bear'}">${p.type==='bullish'?'🟢':'🔴'}</div><div class="pat-info"><div class="pat-name">${p.pattern.replace(/_/g,' ')}</div><div class="pat-date">${(p.date||'').split(' ')[0]} · ₹${(p.price||0).toLocaleString('en-IN')}</div></div><span class="pat-s ${p.type==='bullish'?'bull':'bear'}">${p.type.toUpperCase()} ${(p.strength*100).toFixed(0)}%</span></div>`).join('')}</div>`;
    document.getElementById('rPatterns').innerHTML=html;
}

function renderTargets(targets,price){
    const sc=['conservative','moderate','aggressive'],tfs=['1Y','3Y','5Y','7Y','10Y','15Y','20Y'],cols={conservative:'var(--green)',moderate:'var(--blue)',aggressive:'var(--yellow)'};
    let html=`<div style="overflow-x:auto"><table class="fc-t"><thead><tr><th>Scenario</th>${tfs.map(t=>`<th>${t}</th>`).join('')}</tr></thead><tbody>`;
    sc.forEach(s=>{const d=targets[s]||{};html+=`<tr><td style="font-weight:700;color:${cols[s]}">${s.toUpperCase()}</td>${tfs.map(tf=>{const v=d[tf];return v?`<td><div style="font-weight:700">₹${v.price?.toLocaleString('en-IN',{maximumFractionDigits:0})}</div><div style="font-size:10px;color:var(--green)">+${v.return_pct}% (${v.cagr}%)</div></td>`:'<td>—</td>'}).join('')}</tr>`});
    html+='</tbody></table></div>';
    const nt=targets.near_term||{};
    html+=`<div style="margin-top:14px;font-size:11px;font-weight:700;color:var(--text3);margin-bottom:8px">📅 Near-Term</div><div class="ee-grid">
        <div class="ee-box target"><div class="ee-l">3M Bull</div><div class="ee-v" style="color:var(--green)">₹${(nt['3_month_bull']||0).toLocaleString('en-IN',{maximumFractionDigits:0})}</div></div>
        <div class="ee-box stop"><div class="ee-l">3M Bear</div><div class="ee-v" style="color:var(--red)">₹${(nt['3_month_bear']||0).toLocaleString('en-IN',{maximumFractionDigits:0})}</div></div>
        <div class="ee-box target"><div class="ee-l">6M Bull</div><div class="ee-v" style="color:var(--green)">₹${(nt['6_month_bull']||0).toLocaleString('en-IN',{maximumFractionDigits:0})}</div></div>
        <div class="ee-box stop"><div class="ee-l">6M Bear</div><div class="ee-v" style="color:var(--red)">₹${(nt['6_month_bear']||0).toLocaleString('en-IN',{maximumFractionDigits:0})}</div></div>
        <div class="ee-box target"><div class="ee-l">1Y Bull</div><div class="ee-v" style="color:var(--green)">₹${(nt['1_year_bull']||0).toLocaleString('en-IN',{maximumFractionDigits:0})}</div></div>
        <div class="ee-box stop"><div class="ee-l">1Y Bear</div><div class="ee-v" style="color:var(--red)">₹${(nt['1_year_bear']||0).toLocaleString('en-IN',{maximumFractionDigits:0})}</div></div>
    </div>`;
    document.getElementById('rTargets').innerHTML=html;
}

function renderSIP(sip){
    const s=sip||{};
    document.getElementById('rSIP').innerHTML=`<div style="padding:12px;background:var(--bg);border-radius:10px;border-left:3px solid var(--cyan)">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;font-size:12px">
            <div><span style="color:var(--text3)">Frequency:</span> ${s.recommended_frequency}</div>
            <div><span style="color:var(--text3)">Income %:</span> <span style="color:var(--green);font-weight:700">${s.income_allocation_pct}%</span></div>
            <div><span style="color:var(--text3)">Duration:</span> ${s.duration}</div>
            <div><span style="color:var(--text3)">Best Day:</span> ${s.best_day}</div>
            <div><span style="color:var(--text3)">Min:</span> ${s.minimum_investment}</div>
            <div><span style="color:var(--text3)">Auto:</span> ${s.auto_invest}</div>
        </div>
        ${s.step_up?.note?`<div style="margin-top:8px;font-size:11px;color:var(--text2)">💡 ${s.step_up.note}</div>`:''}
        ${s.platforms?`<div style="margin-top:6px;font-size:10px;color:var(--text3)">Platforms: ${s.platforms.join(' · ')}</div>`:''}
    </div>`;
}

function renderWealth(proj){
    if(!proj){document.getElementById('rWealth').innerHTML='';return}
    const sip=proj.sip||{},show=['₹5,000/month','₹10,000/month','₹25,000/month','₹50,000/month'],yrs=['5Y','10Y','15Y','20Y'];
    let html=`<div style="font-size:11px;font-weight:700;color:var(--text3);margin-bottom:8px">📈 Monthly SIP Growth</div><div style="overflow-x:auto"><table class="fc-t"><thead><tr><th>SIP</th>${yrs.map(y=>`<th>${y}</th>`).join('')}</tr></thead><tbody>`;
    show.forEach(a=>{const d=sip[a];if(!d)return;html+=`<tr><td style="font-weight:700">${a}</td>${yrs.map(y=>{const v=d[y];return v?`<td><div style="font-weight:700">₹${v.future_value.toLocaleString('en-IN',{maximumFractionDigits:0})}</div><div style="font-size:10px;color:var(--green)">+${v.multiplier}x</div></td>`:'<td>—</td>'}).join('')}</tr>`});
    html+='</tbody></table></div>';
    const d10=sip['₹10,000/month']?.['20Y'];
    if(d10)html+=`<div style="margin-top:10px;padding:8px;background:var(--cyan-bg);border-radius:8px;font-size:11px">💡 <strong>₹10K/month × 20Y:</strong> Invest <strong>₹${d10.total_invested.toLocaleString('en-IN',{maximumFractionDigits:0})}</strong> → <strong style="color:var(--green)">₹${d10.future_value.toLocaleString('en-IN',{maximumFractionDigits:0})}</strong> (${d10.multiplier}x)</div>`;
    document.getElementById('rWealth').innerHTML=html;
}

function renderRisk(risks){
    const items=risks.individual_risks||[],overall=risks.overall_risk_level||'UNKNOWN',counts=risks.risk_count||{};
    let html=`<div style="display:flex;gap:10px;align-items:center;margin-bottom:10px;padding:8px;background:var(--bg);border-radius:8px"><span style="font-size:12px;color:var(--text3)">Overall:</span><span class="risk-b ${overall.toLowerCase().replace('_','-')}" style="font-size:14px;padding:4px 12px">${overall.replace(/_/g,' ')}</span><span style="font-size:10px;color:var(--text3)">(${counts.high||0}H · ${counts.medium||0}M · ${counts.low||0}L)</span></div>`;
    items.forEach(r=>{const l=r.level.toLowerCase();html+=`<div class="risk ${l}"><span class="risk-b ${l}">${r.level}</span><div><div class="risk-t">${r.type}</div><div class="risk-d">${r.detail}</div></div></div>`});
    document.getElementById('rRisk').innerHTML=html;
}