/**
 * FutureCandle Charts — Self-contained Canvas charting (no dependencies)
 * Supports: Candlestick, Area/Line, SMA overlays, crosshair
 */
class FCChart {
    constructor(container, opts = {}) {
        this.container = typeof container === 'string' ? document.getElementById(container) : container;
        this.canvas = document.createElement('canvas');
        this.container.appendChild(this.canvas);
        this.ctx = this.canvas.getContext('2d');
        this.data = [];
        this.overlays = []; // [{data:[], color, width, dashed}]
        this.type = 'candle'; // 'candle' | 'area' | 'line'
        this.colors = {
            bg: '#12121a', grid: '#1e1e2e', text: '#6a6e80',
            up: '#26a69a', down: '#ef5350',
            area: '#2962ff', areaBg: 'rgba(41,98,255,0.08)',
            crosshair: '#555', crosshairText: '#e1e4ea'
        };
        this.padding = { top: 20, right: 70, bottom: 30, left: 10 };
        this.mouse = null;
        this._resize();
        this._events();
        this._ro = new ResizeObserver(() => { this._resize(); this.draw(); });
        this._ro.observe(this.container);
    }

    _resize() {
        const r = this.container.getBoundingClientRect();
        this.w = r.width;
        this.h = r.height || 380;
        this.canvas.width = this.w * devicePixelRatio;
        this.canvas.height = this.h * devicePixelRatio;
        this.canvas.style.width = this.w + 'px';
        this.canvas.style.height = this.h + 'px';
        this.ctx.scale(devicePixelRatio, devicePixelRatio);
    }

    _events() {
        this.canvas.addEventListener('mousemove', e => {
            const r = this.canvas.getBoundingClientRect();
            this.mouse = { x: e.clientX - r.left, y: e.clientY - r.top };
            this.draw();
        });
        this.canvas.addEventListener('mouseleave', () => { this.mouse = null; this.draw(); });
    }

    setData(data) {
        // data = [{time, open, high, low, close}] or [{time, value}]
        this.data = data;
        this.draw();
    }

    addOverlay(data, color, width = 1, dashed = true) {
        this.overlays.push({ data, color, width, dashed });
        this.draw();
    }

    clearOverlays() { this.overlays = []; }

    _chartArea() {
        return {
            x: this.padding.left,
            y: this.padding.top,
            w: this.w - this.padding.left - this.padding.right,
            h: this.h - this.padding.top - this.padding.bottom
        };
    }

    _priceRange() {
        let min = Infinity, max = -Infinity;
        const d = this.data;
        for (let i = 0; i < d.length; i++) {
            const item = d[i];
            if (item.high !== undefined) {
                if (item.high > max) max = item.high;
                if (item.low < min) min = item.low;
            } else if (item.value !== undefined) {
                if (item.value > max) max = item.value;
                if (item.value < min) min = item.value;
            }
        }
        // Include overlays
        this.overlays.forEach(o => {
            o.data.forEach(p => {
                if (p.value > max) max = p.value;
                if (p.value < min) min = p.value;
            });
        });
        const pad = (max - min) * 0.05;
        return { min: min - pad, max: max + pad };
    }

    _xScale(i) {
        const a = this._chartArea();
        return a.x + (i / Math.max(this.data.length - 1, 1)) * a.w;
    }

    _yScale(price) {
        const a = this._chartArea();
        const r = this._priceRange();
        return a.y + a.h - ((price - r.min) / (r.max - r.min)) * a.h;
    }

    _priceFromY(y) {
        const a = this._chartArea();
        const r = this._priceRange();
        return r.min + ((a.y + a.h - y) / a.h) * (r.max - r.min);
    }

    _indexFromX(x) {
        const a = this._chartArea();
        return Math.round(((x - a.x) / a.w) * (this.data.length - 1));
    }

    draw() {
        const ctx = this.ctx;
        const w = this.w, h = this.h;
        const a = this._chartArea();
        const range = this._priceRange();

        // Clear
        ctx.fillStyle = this.colors.bg;
        ctx.fillRect(0, 0, w, h);

        if (!this.data.length) {
            ctx.fillStyle = this.colors.text;
            ctx.font = '14px sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('No data loaded', w/2, h/2);
            return;
        }

        // Grid lines
        ctx.strokeStyle = this.colors.grid;
        ctx.lineWidth = 1;
        const priceStep = this._niceStep(range.max - range.min, 6);
        ctx.font = '10px sans-serif';
        ctx.textAlign = 'right';
        ctx.fillStyle = this.colors.text;
        for (let p = Math.ceil(range.min / priceStep) * priceStep; p <= range.max; p += priceStep) {
            const y = this._yScale(p);
            ctx.beginPath(); ctx.moveTo(a.x, y); ctx.lineTo(a.x + a.w, y); ctx.stroke();
            ctx.fillText(this._formatPrice(p), a.x + a.w + 65, y + 3);
        }

        // Date labels
        ctx.textAlign = 'center';
        const step = Math.max(1, Math.floor(this.data.length / 8));
        for (let i = 0; i < this.data.length; i += step) {
            const x = this._xScale(i);
            ctx.fillText(this.data[i].time.substring(5), x, a.y + a.h + 18);
        }

        // Draw data
        if (this.type === 'candle') this._drawCandles(ctx, a, range);
        else this._drawArea(ctx, a, range);

        // Overlays
        this.overlays.forEach(o => {
            ctx.strokeStyle = o.color;
            ctx.lineWidth = o.width;
            ctx.setLineDash(o.dashed ? [4, 4] : []);
            ctx.beginPath();
            o.data.forEach((p, i) => {
                const x = this._xScale(i);
                const y = this._yScale(p.value);
                i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
            });
            ctx.stroke();
            ctx.setLineDash([]);
        });

        // Crosshair
        if (this.mouse && this.mouse.x >= a.x && this.mouse.x <= a.x + a.w && this.mouse.y >= a.y && this.mouse.y <= a.y + a.h) {
            const idx = Math.min(Math.max(0, this._indexFromX(this.mouse.x)), this.data.length - 1);
            const item = this.data[idx];
            const x = this._xScale(idx);

            ctx.strokeStyle = this.colors.crosshair;
            ctx.lineWidth = 0.5;
            ctx.setLineDash([3, 3]);
            ctx.beginPath(); ctx.moveTo(x, a.y); ctx.lineTo(x, a.y + a.h); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(a.x, this.mouse.y); ctx.lineTo(a.x + a.w, this.mouse.y); ctx.stroke();
            ctx.setLineDash([]);

            // Price label
            const price = this._priceFromY(this.mouse.y);
            ctx.fillStyle = '#333';
            ctx.fillRect(a.x + a.w + 2, this.mouse.y - 9, 68, 18);
            ctx.fillStyle = this.colors.crosshairText;
            ctx.font = '10px monospace';
            ctx.textAlign = 'right';
            ctx.fillText(this._formatPrice(price), a.x + a.w + 65, this.mouse.y + 4);

            // OHLCV info bar
            if (item) {
                ctx.fillStyle = 'rgba(18,18,26,0.9)';
                ctx.fillRect(a.x, a.y - 18, a.w, 16);
                ctx.fillStyle = this.colors.text;
                ctx.font = '10px monospace';
                ctx.textAlign = 'left';
                let txt = item.time;
                if (item.open !== undefined) {
                    txt += `   O:${this._formatPrice(item.open)}  H:${this._formatPrice(item.high)}  L:${this._formatPrice(item.low)}  C:${this._formatPrice(item.close)}`;
                } else {
                    txt += `   V:${this._formatPrice(item.value)}`;
                }
                ctx.fillText(txt, a.x + 4, a.y - 6);
            }
        }
    }

    _drawCandles(ctx, a, range) {
        const data = this.data;
        const bw = Math.max(1, (a.w / data.length) * 0.6);
        for (let i = 0; i < data.length; i++) {
            const d = data[i];
            const x = this._xScale(i);
            const yO = this._yScale(d.open);
            const yC = this._yScale(d.close);
            const yH = this._yScale(d.high);
            const yL = this._yScale(d.low);
            const bull = d.close >= d.open;
            ctx.strokeStyle = bull ? this.colors.up : this.colors.down;
            ctx.fillStyle = bull ? this.colors.up : this.colors.down;

            // Wick
            ctx.beginPath();
            ctx.moveTo(x, yH);
            ctx.lineTo(x, yL);
            ctx.lineWidth = 1;
            ctx.stroke();

            // Body
            const bodyTop = Math.min(yO, yC);
            const bodyH = Math.max(Math.abs(yC - yO), 1);
            if (bull) {
                ctx.fillRect(x - bw/2, bodyTop, bw, bodyH);
            } else {
                ctx.fillRect(x - bw/2, bodyTop, bw, bodyH);
            }
        }
    }

    _drawArea(ctx, a, range) {
        const data = this.data;
        ctx.beginPath();
        for (let i = 0; i < data.length; i++) {
            const v = data[i].value !== undefined ? data[i].value : data[i].close;
            const x = this._xScale(i);
            const y = this._yScale(v);
            i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        }

        // Fill
        ctx.lineTo(this._xScale(data.length - 1), a.y + a.h);
        ctx.lineTo(this._xScale(0), a.y + a.h);
        ctx.closePath();
        ctx.fillStyle = this.colors.areaBg;
        ctx.fill();

        // Stroke
        ctx.beginPath();
        for (let i = 0; i < data.length; i++) {
            const v = data[i].value !== undefined ? data[i].value : data[i].close;
            const x = this._xScale(i);
            const y = this._yScale(v);
            i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
        }
        ctx.strokeStyle = this.colors.area;
        ctx.lineWidth = 2;
        ctx.stroke();
    }

    setType(type) {
        this.type = type;
        this.draw();
    }

    destroy() {
        if (this._ro) this._ro.disconnect();
        if (this.canvas && this.canvas.parentNode) this.canvas.parentNode.removeChild(this.canvas);
    }

    _formatPrice(p) {
        if (p === undefined || p === null) return '—';
        if (Math.abs(p) >= 1000) return p.toLocaleString('en-IN', { maximumFractionDigits: 0 });
        if (Math.abs(p) >= 100) return p.toFixed(1);
        return p.toFixed(2);
    }

    _niceStep(range, targetSteps) {
        const rough = range / targetSteps;
        const pow = Math.pow(10, Math.floor(Math.log10(rough)));
        const frac = rough / pow;
        let nice;
        if (frac <= 1.5) nice = 1;
        else if (frac <= 3) nice = 2;
        else if (frac <= 7) nice = 5;
        else nice = 10;
        return nice * pow;
    }

    // Helper: compute SMA
    static computeSMA(closes, period) {
        const result = [];
        for (let i = 0; i < closes.length; i++) {
            if (i < period - 1) { result.push(null); continue; }
            let sum = 0;
            for (let j = 0; j < period; j++) sum += (closes[i-j].value !== undefined ? closes[i-j].value : closes[i-j].close || closes[i-j]);
            result.push({ time: closes[i].time, value: sum / period });
        }
        return result.filter(x => x !== null);
    }
}