"""
Technical Analysis Engine
Comprehensive technical indicators for Indian stock market analysis
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple


class TechnicalAnalysisEngine:
    """Advanced technical analysis with 25+ indicators."""

    def __init__(self):
        self.indicators = {}

    def calculate_all(self, df: pd.DataFrame) -> Dict:
        """Calculate all technical indicators."""
        result = {}
        closes = df['Close'].values
        highs = df['High'].values
        lows = df['Low'].values
        opens = df['Open'].values
        volumes = df['Volume'].values if 'Volume' in df.columns else np.ones(len(df))

        result['moving_averages'] = self._moving_averages(closes)
        result['rsi'] = self._rsi(closes, 14)
        result['macd'] = self._macd(closes)
        result['bollinger_bands'] = self._bollinger_bands(closes)
        result['stochastic'] = self._stochastic(highs, lows, closes)
        result['atr'] = self._atr(highs, lows, closes)
        result['adx'] = self._adx(highs, lows, closes)
        result['obv'] = self._obv(closes, volumes)
        result['vwap'] = self._vwap(highs, lows, closes, volumes)
        result['ichimoku'] = self._ichimoku(highs, lows, closes)
        result['supertrend'] = self._supertrend(highs, lows, closes)
        result['pivot_points'] = self._pivot_points(highs[-1], lows[-1], closes[-1])
        result['fibonacci'] = self._fibonacci_levels(highs, lows)
        result['williams_r'] = self._williams_r(highs, lows, closes)
        result['cci'] = self._cci(highs, lows, closes)
        result['mfi'] = self._mfi(highs, lows, closes, volumes)
        result['roc'] = self._roc(closes)
        result['volume_analysis'] = self._volume_analysis(volumes, closes)
        result['trend_strength'] = self._trend_strength(closes, highs, lows)
        result['support_resistance'] = self._support_resistance(closes, highs, lows)

        # Overall technical score
        result['overall_score'] = self._calculate_overall_score(result)
        result['signal'] = self._generate_signal(result)

        return result

    def _moving_averages(self, closes: np.ndarray) -> Dict:
        """Calculate multiple moving averages."""
        result = {}
        for period in [5, 10, 20, 50, 100, 200]:
            if len(closes) >= period:
                ma = np.mean(closes[-period:])
                result[f'SMA_{period}'] = round(float(ma), 2)
                result[f'SMA_{period}_signal'] = 'BULLISH' if closes[-1] > ma else 'BEARISH'

        # EMA
        for period in [9, 12, 21, 26, 50]:
            if len(closes) >= period:
                multiplier = 2 / (period + 1)
                ema = closes[0]
                for price in closes[1:]:
                    ema = (price - ema) * multiplier + ema
                result[f'EMA_{period}'] = round(float(ema), 2)
                result[f'EMA_{period}_signal'] = 'BULLISH' if closes[-1] > ema else 'BEARISH'

        # Golden/Death Cross
        if len(closes) >= 200:
            sma50 = np.mean(closes[-50:])
            sma200 = np.mean(closes[-200:])
            if sma50 > sma200:
                result['cross_signal'] = 'GOLDEN_CROSS (Bullish)'
            else:
                result['cross_signal'] = 'DEATH_CROSS (Bearish)'

        return result

    def _rsi(self, closes: np.ndarray, period: int = 14) -> Dict:
        """Relative Strength Index."""
        if len(closes) < period + 1:
            return {'value': 50, 'signal': 'NEUTRAL', 'zone': 'NEUTRAL'}

        deltas = np.diff(closes)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)

        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])

        if avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

        if rsi > 70:
            signal, zone = 'OVERBOUGHT', 'OVERBOUGHT'
        elif rsi > 60:
            signal, zone = 'BULLISH', 'BULLISH'
        elif rsi < 30:
            signal, zone = 'OVERSOLD', 'OVERSOLD'
        elif rsi < 40:
            signal, zone = 'BEARISH', 'BEARISH'
        else:
            signal, zone = 'NEUTRAL', 'NEUTRAL'

        return {
            'value': round(float(rsi), 2),
            'signal': signal,
            'zone': zone,
            'period': period
        }

    def _macd(self, closes: np.ndarray) -> Dict:
        """MACD indicator."""
        if len(closes) < 26:
            return {'signal': 'NEUTRAL', 'histogram': 0}

        def ema(data, period):
            multiplier = 2 / (period + 1)
            result = [data[0]]
            for i in range(1, len(data)):
                result.append((data[i] - result[-1]) * multiplier + result[-1])
            return np.array(result)

        ema12 = ema(closes, 12)
        ema26 = ema(closes, 26)
        macd_line = ema12 - ema26
        signal_line = ema(macd_line, 9)
        histogram = macd_line - signal_line

        macd_val = float(macd_line[-1])
        signal_val = float(signal_line[-1])
        hist_val = float(histogram[-1])

        if hist_val > 0 and histogram[-2] <= 0:
            sig = 'BULLISH_CROSSOVER'
        elif hist_val < 0 and histogram[-2] >= 0:
            sig = 'BEARISH_CROSSOVER'
        elif hist_val > 0:
            sig = 'BULLISH'
        elif hist_val < 0:
            sig = 'BEARISH'
        else:
            sig = 'NEUTRAL'

        return {
            'macd': round(macd_val, 4),
            'signal': round(signal_val, 4),
            'histogram': round(hist_val, 4),
            'signal_type': sig
        }

    def _bollinger_bands(self, closes: np.ndarray, period: int = 20) -> Dict:
        """Bollinger Bands."""
        if len(closes) < period:
            return {'signal': 'NEUTRAL'}

        sma = np.mean(closes[-period:])
        std = np.std(closes[-period:])
        upper = sma + 2 * std
        lower = sma - 2 * std
        current = closes[-1]

        if current > upper:
            signal = 'OVERBOUGHT'
        elif current < lower:
            signal = 'OVERSOLD'
        elif current > sma:
            signal = 'BULLISH'
        else:
            signal = 'BEARISH'

        # Bandwidth (volatility)
        bandwidth = (upper - lower) / sma * 100

        return {
            'upper': round(float(upper), 2),
            'middle': round(float(sma), 2),
            'lower': round(float(lower), 2),
            'bandwidth': round(float(bandwidth), 2),
            'signal': signal,
            'price_position': round(float((current - lower) / (upper - lower) * 100), 1)
        }

    def _stochastic(self, highs: np.ndarray, lows: np.ndarray, closes: np.ndarray, period: int = 14) -> Dict:
        """Stochastic Oscillator."""
        if len(closes) < period:
            return {'signal': 'NEUTRAL'}

        highest = np.max(highs[-period:])
        lowest = np.min(lows[-period:])
        k = ((closes[-1] - lowest) / (highest - lowest)) * 100 if (highest - lowest) != 0 else 50

        # Simple 3-period %D
        k_values = []
        for i in range(max(0, len(closes)-3), len(closes)):
            h = np.max(highs[max(0,i-period+1):i+1])
            l = np.min(lows[max(0,i-period+1):i+1])
            k_val = ((closes[i] - l) / (h - l)) * 100 if (h - l) != 0 else 50
            k_values.append(k_val)
        d = np.mean(k_values)

        if k > 80:
            signal = 'OVERBOUGHT'
        elif k < 20:
            signal = 'OVERSOLD'
        else:
            signal = 'NEUTRAL'

        return {'k': round(float(k), 2), 'd': round(float(d), 2), 'signal': signal}

    def _atr(self, highs: np.ndarray, lows: np.ndarray, closes: np.ndarray, period: int = 14) -> Dict:
        """Average True Range."""
        if len(closes) < 2:
            return {'value': 0, 'volatility': 'LOW'}

        tr_list = []
        for i in range(1, len(closes)):
            tr = max(
                highs[i] - lows[i],
                abs(highs[i] - closes[i-1]),
                abs(lows[i] - closes[i-1])
            )
            tr_list.append(tr)

        atr = np.mean(tr_list[-period:]) if len(tr_list) >= period else np.mean(tr_list)
        atr_pct = (atr / closes[-1]) * 100

        if atr_pct > 3:
            vol = 'VERY_HIGH'
        elif atr_pct > 2:
            vol = 'HIGH'
        elif atr_pct > 1:
            vol = 'MODERATE'
        else:
            vol = 'LOW'

        return {'value': round(float(atr), 2), 'percentage': round(float(atr_pct), 2), 'volatility': vol}

    def _adx(self, highs: np.ndarray, lows: np.ndarray, closes: np.ndarray, period: int = 14) -> Dict:
        """Average Directional Index."""
        if len(closes) < period + 1:
            return {'value': 25, 'trend': 'WEAK'}

        plus_dm = []
        minus_dm = []
        tr_list = []

        for i in range(1, len(closes)):
            up_move = highs[i] - highs[i-1]
            down_move = lows[i-1] - lows[i]
            plus_dm.append(up_move if up_move > down_move and up_move > 0 else 0)
            minus_dm.append(down_move if down_move > up_move and down_move > 0 else 0)
            tr = max(highs[i]-lows[i], abs(highs[i]-closes[i-1]), abs(lows[i]-closes[i-1]))
            tr_list.append(tr)

        atr = np.mean(tr_list[-period:])
        plus_di = (np.mean(plus_dm[-period:]) / atr) * 100 if atr > 0 else 0
        minus_di = (np.mean(minus_dm[-period:]) / atr) * 100 if atr > 0 else 0

        dx = abs(plus_di - minus_di) / (plus_di + minus_di) * 100 if (plus_di + minus_di) > 0 else 0

        if dx > 40:
            trend = 'VERY_STRONG'
        elif dx > 25:
            trend = 'STRONG'
        elif dx > 20:
            trend = 'MODERATE'
        else:
            trend = 'WEAK'

        direction = 'BULLISH' if plus_di > minus_di else 'BEARISH'

        return {
            'value': round(float(dx), 2),
            'plus_di': round(float(plus_di), 2),
            'minus_di': round(float(minus_di), 2),
            'trend': trend,
            'direction': direction
        }

    def _obv(self, closes: np.ndarray, volumes: np.ndarray) -> Dict:
        """On Balance Volume."""
        obv = [0]
        for i in range(1, len(closes)):
            if closes[i] > closes[i-1]:
                obv.append(obv[-1] + volumes[i])
            elif closes[i] < closes[i-1]:
                obv.append(obv[-1] - volumes[i])
            else:
                obv.append(obv[-1])

        obv_arr = np.array(obv)
        obv_sma = np.mean(obv_arr[-20:]) if len(obv_arr) > 20 else np.mean(obv_arr)

        signal = 'BULLISH' if obv_arr[-1] > obv_sma else 'BEARISH'

        return {'value': round(float(obv_arr[-1]), 0), 'sma_20': round(float(obv_sma), 0), 'signal': signal}

    def _vwap(self, highs: np.ndarray, lows: np.ndarray, closes: np.ndarray, volumes: np.ndarray) -> Dict:
        """Volume Weighted Average Price."""
        typical_price = (highs + lows + closes) / 3
        cumulative_tp_vol = np.cumsum(typical_price * volumes)
        cumulative_vol = np.cumsum(volumes)
        vwap = cumulative_tp_vol / cumulative_vol if cumulative_vol[-1] != 0 else closes[-1]

        signal = 'BULLISH' if closes[-1] > vwap[-1] else 'BEARISH'

        return {'value': round(float(vwap[-1]), 2), 'signal': signal}

    def _ichimoku(self, highs: np.ndarray, lows: np.ndarray, closes: np.ndarray) -> Dict:
        """Ichimoku Cloud."""
        if len(closes) < 52:
            return {'signal': 'NEUTRAL'}

        tenkan = (np.max(highs[-9:]) + np.min(lows[-9:])) / 2
        kijun = (np.max(highs[-26:]) + np.min(lows[-26:])) / 2
        senkou_a = (tenkan + kijun) / 2
        senkou_b = (np.max(highs[-52:]) + np.min(lows[-52:])) / 2

        cloud_top = max(senkou_a, senkou_b)
        cloud_bottom = min(senkou_a, senkou_b)

        if closes[-1] > cloud_top:
            signal = 'BULLISH'
        elif closes[-1] < cloud_bottom:
            signal = 'BEARISH'
        else:
            signal = 'IN_CLOUD'

        tk_cross = 'BULLISH' if tenkan > kijun else 'BEARISH'

        return {
            'tenkan_sen': round(float(tenkan), 2),
            'kijun_sen': round(float(kijun), 2),
            'senkou_a': round(float(senkou_a), 2),
            'senkou_b': round(float(senkou_b), 2),
            'signal': signal,
            'tk_cross': tk_cross
        }

    def _supertrend(self, highs: np.ndarray, lows: np.ndarray, closes: np.ndarray, period: int = 10, multiplier: float = 3.0) -> Dict:
        """Supertrend indicator."""
        if len(closes) < period + 1:
            return {'signal': 'NEUTRAL'}

        tr_list = []
        for i in range(1, len(closes)):
            tr = max(highs[i]-lows[i], abs(highs[i]-closes[i-1]), abs(lows[i]-closes[i-1]))
            tr_list.append(tr)

        atr = np.mean(tr_list[-period:])
        upper_band = (highs[-1] + lows[-1]) / 2 + multiplier * atr
        lower_band = (highs[-1] + lows[-1]) / 2 - multiplier * atr

        if closes[-1] > upper_band:
            signal = 'BULLISH'
        elif closes[-1] < lower_band:
            signal = 'BEARISH'
        else:
            signal = 'NEUTRAL'

        return {
            'upper_band': round(float(upper_band), 2),
            'lower_band': round(float(lower_band), 2),
            'signal': signal
        }

    def _pivot_points(self, high: float, low: float, close: float) -> Dict:
        """Pivot Points."""
        pivot = (high + low + close) / 3
        r1 = 2 * pivot - low
        r2 = pivot + (high - low)
        r3 = high + 2 * (pivot - low)
        s1 = 2 * pivot - high
        s2 = pivot - (high - low)
        s3 = low - 2 * (high - pivot)

        return {
            'pivot': round(pivot, 2),
            'r1': round(r1, 2), 'r2': round(r2, 2), 'r3': round(r3, 2),
            's1': round(s1, 2), 's2': round(s2, 2), 's3': round(s3, 2)
        }

    def _fibonacci_levels(self, highs: np.ndarray, lows: np.ndarray) -> Dict:
        """Fibonacci Retracement Levels."""
        high = np.max(highs[-100:]) if len(highs) >= 100 else np.max(highs)
        low = np.min(lows[-100:]) if len(lows) >= 100 else np.min(lows)
        diff = high - low

        levels = {
            '0.0%': round(low, 2),
            '23.6%': round(low + 0.236 * diff, 2),
            '38.2%': round(low + 0.382 * diff, 2),
            '50.0%': round(low + 0.5 * diff, 2),
            '61.8%': round(low + 0.618 * diff, 2),
            '78.6%': round(low + 0.786 * diff, 2),
            '100.0%': round(high, 2)
        }
        return levels

    def _williams_r(self, highs: np.ndarray, lows: np.ndarray, closes: np.ndarray, period: int = 14) -> Dict:
        """Williams %R."""
        if len(closes) < period:
            return {'value': -50, 'signal': 'NEUTRAL'}

        highest = np.max(highs[-period:])
        lowest = np.min(lows[-period:])
        wr = ((highest - closes[-1]) / (highest - lowest)) * -100 if (highest - lowest) != 0 else -50

        if wr > -20:
            signal = 'OVERBOUGHT'
        elif wr < -80:
            signal = 'OVERSOLD'
        else:
            signal = 'NEUTRAL'

        return {'value': round(float(wr), 2), 'signal': signal}

    def _cci(self, highs: np.ndarray, lows: np.ndarray, closes: np.ndarray, period: int = 20) -> Dict:
        """Commodity Channel Index."""
        if len(closes) < period:
            return {'value': 0, 'signal': 'NEUTRAL'}

        tp = (highs[-period:] + lows[-period:] + closes[-period:]) / 3
        tp_mean = np.mean(tp)
        tp_mad = np.mean(np.abs(tp - tp_mean))
        cci = (tp[-1] - tp_mean) / (0.015 * tp_mad) if tp_mad != 0 else 0

        if cci > 100:
            signal = 'OVERBOUGHT'
        elif cci < -100:
            signal = 'OVERSOLD'
        else:
            signal = 'NEUTRAL'

        return {'value': round(float(cci), 2), 'signal': signal}

    def _mfi(self, highs: np.ndarray, lows: np.ndarray, closes: np.ndarray, volumes: np.ndarray, period: int = 14) -> Dict:
        """Money Flow Index."""
        if len(closes) < period + 1:
            return {'value': 50, 'signal': 'NEUTRAL'}

        tp = (highs + lows + closes) / 3
        mf = tp * volumes

        pos_mf = 0
        neg_mf = 0
        for i in range(-period, 0):
            if tp[i] > tp[i-1]:
                pos_mf += mf[i]
            else:
                neg_mf += mf[i]

        mfi = 100 - (100 / (1 + pos_mf / neg_mf)) if neg_mf != 0 else 100

        if mfi > 80:
            signal = 'OVERBOUGHT'
        elif mfi < 20:
            signal = 'OVERSOLD'
        else:
            signal = 'NEUTRAL'

        return {'value': round(float(mfi), 2), 'signal': signal}

    def _roc(self, closes: np.ndarray, period: int = 12) -> Dict:
        """Rate of Change."""
        if len(closes) < period + 1:
            return {'value': 0, 'signal': 'NEUTRAL'}

        roc = ((closes[-1] - closes[-period]) / closes[-period]) * 100

        signal = 'BULLISH' if roc > 0 else 'BEARISH'

        return {'value': round(float(roc), 2), 'signal': signal}

    def _volume_analysis(self, volumes: np.ndarray, closes: np.ndarray) -> Dict:
        """Volume analysis."""
        avg_vol = np.mean(volumes[-20:]) if len(volumes) >= 20 else np.mean(volumes)
        current_vol = volumes[-1]
        ratio = current_vol / avg_vol if avg_vol > 0 else 1

        if ratio > 2:
            signal = 'HIGH_VOLUME'
        elif ratio > 1.5:
            signal = 'ABOVE_AVERAGE'
        elif ratio < 0.5:
            signal = 'LOW_VOLUME'
        else:
            signal = 'NORMAL'

        # Volume trend
        vol_sma_5 = np.mean(volumes[-5:])
        vol_sma_20 = np.mean(volumes[-20:]) if len(volumes) >= 20 else np.mean(volumes)
        vol_trend = 'INCREASING' if vol_sma_5 > vol_sma_20 else 'DECREASING'

        return {
            'current': int(current_vol),
            'average_20d': int(avg_vol),
            'ratio': round(float(ratio), 2),
            'signal': signal,
            'trend': vol_trend
        }

    def _trend_strength(self, closes: np.ndarray, highs: np.ndarray, lows: np.ndarray) -> Dict:
        """Overall trend strength analysis."""
        if len(closes) < 50:
            return {'strength': 'UNKNOWN', 'direction': 'NEUTRAL'}

        # Linear regression slope
        x = np.arange(len(closes[-100:])) if len(closes) >= 100 else np.arange(len(closes))
        y = closes[-100:] if len(closes) >= 100 else closes
        slope = np.polyfit(x, y, 1)[0]

        # Normalize slope
        avg_price = np.mean(y)
        slope_pct = (slope / avg_price) * 100

        # Higher highs / Lower lows
        recent_high = np.max(highs[-20:])
        prev_high = np.max(highs[-40:-20]) if len(highs) >= 40 else recent_high
        recent_low = np.min(lows[-20:])
        prev_low = np.min(lows[-40:-20]) if len(lows) >= 40 else recent_low

        higher_highs = recent_high > prev_high
        higher_lows = recent_low > prev_low

        if higher_highs and higher_lows:
            pattern = 'UPTREND'
        elif not higher_highs and not higher_lows:
            pattern = 'DOWNTREND'
        else:
            pattern = 'SIDEWAYS'

        if slope_pct > 0.1:
            direction = 'STRONG_BULLISH'
        elif slope_pct > 0.03:
            direction = 'BULLISH'
        elif slope_pct < -0.1:
            direction = 'STRONG_BEARISH'
        elif slope_pct < -0.03:
            direction = 'BEARISH'
        else:
            direction = 'NEUTRAL'

        return {
            'slope': round(float(slope), 4),
            'slope_percentage': round(float(slope_pct), 4),
            'direction': direction,
            'pattern': pattern,
            'higher_highs': higher_highs,
            'higher_lows': higher_lows
        }

    def _support_resistance(self, closes: np.ndarray, highs: np.ndarray, lows: np.ndarray) -> Dict:
        """Key support and resistance levels."""
        recent = closes[-100:] if len(closes) >= 100 else closes
        recent_h = highs[-100:] if len(highs) >= 100 else highs
        recent_l = lows[-100:] if len(lows) >= 100 else lows
        current = closes[-1]

        # Simple pivot-based S/R
        pivot = (recent_h[-1] + recent_l[-1] + recent[-1]) / 3

        supports = sorted([
            round(float(2 * pivot - recent_h[-1]), 2),
            round(float(pivot - (recent_h[-1] - recent_l[-1])), 2),
            round(float(np.min(recent_l[-20:])), 2),
            round(float(np.min(recent_l[-50:])) if len(recent_l) >= 50 else float(np.min(recent_l)), 2)
        ])

        resistances = sorted([
            round(float(2 * pivot - recent_l[-1]), 2),
            round(float(pivot + (recent_h[-1] - recent_l[-1])), 2),
            round(float(np.max(recent_h[-20:])), 2),
            round(float(np.max(recent_h[-50:])) if len(recent_h) >= 50 else float(np.max(recent_h)), 2)
        ])

        # Nearest support and resistance
        nearest_support = max([s for s in supports if s < current], default=supports[0])
        nearest_resistance = min([r for r in resistances if r > current], default=resistances[-1])

        return {
            'supports': supports,
            'resistances': resistances,
            'nearest_support': nearest_support,
            'nearest_resistance': nearest_resistance
        }

    def _calculate_overall_score(self, result: Dict) -> float:
        """Calculate overall technical score (0-100)."""
        scores = []
        weights = {
            'rsi': 15, 'macd': 15, 'bollinger_bands': 10,
            'stochastic': 10, 'adx': 10, 'ichimoku': 10,
            'supertrend': 10, 'volume_analysis': 10, 'trend_strength': 10
        }

        # RSI
        rsi_val = result.get('rsi', {}).get('value', 50)
        if rsi_val > 50:
            scores.append(min(rsi_val, 80) / 80 * weights['rsi'])
        else:
            scores.append(max(rsi_val, 20) / 80 * weights['rsi'])

        # MACD
        macd_sig = result.get('macd', {}).get('signal_type', 'NEUTRAL')
        if 'BULLISH' in macd_sig:
            scores.append(weights['macd'] * 0.75)
        elif 'BEARISH' in macd_sig:
            scores.append(weights['macd'] * 0.25)
        else:
            scores.append(weights['macd'] * 0.5)

        # Bollinger
        bb_sig = result.get('bollinger_bands', {}).get('signal', 'NEUTRAL')
        bb_map = {'OVERSOLD': 0.7, 'BULLISH': 0.65, 'NEUTRAL': 0.5, 'BEARISH': 0.35, 'OVERBOUGHT': 0.3}
        scores.append(weights['bollinger_bands'] * bb_map.get(bb_sig, 0.5))

        # Stochastic
        stoch = result.get('stochastic', {}).get('k', 50)
        scores.append(weights['stochastic'] * (stoch / 100))

        # ADX
        adx = result.get('adx', {})
        adx_val = adx.get('value', 25)
        adx_dir = adx.get('direction', 'NEUTRAL')
        adx_weight = min(adx_val / 50, 1.0) * weights['adx']
        scores.append(adx_weight * (0.75 if adx_dir == 'BULLISH' else 0.25))

        # Ichimoku
        ichi = result.get('ichimoku', {}).get('signal', 'NEUTRAL')
        ichi_map = {'BULLISH': 0.75, 'BEARISH': 0.25, 'IN_CLOUD': 0.5}
        scores.append(weights['ichimoku'] * ichi_map.get(ichi, 0.5))

        # Supertrend
        st_sig = result.get('supertrend', {}).get('signal', 'NEUTRAL')
        st_map = {'BULLISH': 0.75, 'BEARISH': 0.25, 'NEUTRAL': 0.5}
        scores.append(weights['supertrend'] * st_map.get(st_sig, 0.5))

        # Volume
        vol = result.get('volume_analysis', {})
        vol_sig = vol.get('signal', 'NORMAL')
        vol_trend = vol.get('trend', 'DECREASING')
        vol_score = 0.5
        if vol_trend == 'INCREASING':
            vol_score = 0.65
        scores.append(weights['volume_analysis'] * vol_score)

        # Trend strength
        ts = result.get('trend_strength', {})
        ts_dir = ts.get('direction', 'NEUTRAL')
        ts_map = {'STRONG_BULLISH': 0.9, 'BULLISH': 0.7, 'NEUTRAL': 0.5, 'BEARISH': 0.3, 'STRONG_BEARISH': 0.1}
        scores.append(weights['trend_strength'] * ts_map.get(ts_dir, 0.5))

        total_weight = sum(weights.values())
        return round(sum(scores) / total_weight * 100, 1) if total_weight > 0 else 50.0

    def _generate_signal(self, result: Dict) -> Dict:
        """Generate final trading signal."""
        score = result['overall_score']

        if score >= 75:
            action = 'STRONG_BUY'
            confidence = min(score, 95)
        elif score >= 60:
            action = 'BUY'
            confidence = score
        elif score >= 45:
            action = 'HOLD'
            confidence = 50 + abs(score - 50)
        elif score >= 30:
            action = 'SELL'
            confidence = 100 - score
        else:
            action = 'STRONG_SELL'
            confidence = min(100 - score, 95)

        return {
            'action': action,
            'score': score,
            'confidence': round(confidence, 1)
        }