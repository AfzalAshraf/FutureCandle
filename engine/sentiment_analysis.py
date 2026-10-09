"""
Sentiment Analysis Engine
Market sentiment analysis for Indian stocks using news, social signals, and market indicators
"""
import numpy as np
from typing import Dict, List
from datetime import datetime


class SentimentAnalysisEngine:
    """Sentiment analysis for Indian stock market."""

    # Indian market sector sentiment keywords
    POSITIVE_KEYWORDS = [
        'bullish', 'rally', 'surge', 'breakout', 'upgrade', 'outperform',
        'strong results', 'profit growth', 'revenue growth', 'market leader',
        'innovation', 'expansion', 'dividend', 'buyback', 'positive outlook',
        'demand growth', 'order book', 'government support', 'policy boost',
        'FDI inflow', 'record high', 'all time high', '52-week high',
        'sector leader', 'moat', 'competitive advantage', 'margin expansion',
        'debt reduction', 'cash flow', 'return on equity', 'value buy',
        'multibagger', 'wealth creator', 'consistent performer'
    ]

    NEGATIVE_KEYWORDS = [
        'bearish', 'crash', 'decline', 'breakdown', 'downgrade', 'underperform',
        'weak results', 'profit decline', 'revenue fall', 'market share loss',
        'competition', 'shutdown', 'debt', 'default', 'negative outlook',
        'demand slowdown', 'order cancellation', 'regulatory risk', 'policy headwind',
        'FII outflow', 'record low', '52-week low', 'insolvency', 'fraud',
        'margin pressure', 'cash burn', 'NPA', 'impairment', 'overvalued',
        'wealth destroyer', 'consistent underperformer', 'management issues'
    ]

    # Indian market specific weights
    SECTOR_WEIGHTS = {
        'IT': {'growth_factor': 1.1, 'stability': 0.85},
        'Banking': {'growth_factor': 1.15, 'stability': 0.7},
        'Pharma': {'growth_factor': 1.05, 'stability': 0.9},
        'FMCG': {'growth_factor': 1.0, 'stability': 0.95},
        'Auto': {'growth_factor': 1.2, 'stability': 0.65},
        'Energy': {'growth_factor': 1.25, 'stability': 0.6},
        'Metals': {'growth_factor': 1.35, 'stability': 0.5},
        'Realty': {'growth_factor': 1.3, 'stability': 0.55},
        'Infra': {'growth_factor': 1.2, 'stability': 0.6},
        'Defense': {'growth_factor': 1.15, 'stability': 0.75},
        'Cement': {'growth_factor': 1.1, 'stability': 0.8},
        'Telecom': {'growth_factor': 1.2, 'stability': 0.65},
        'General': {'growth_factor': 1.1, 'stability': 0.7}
    }

    def __init__(self):
        self.sentiment_history = []

    def analyze(self, symbol: str, current_price: float, technical_data: Dict,
                candlestick_data: Dict, sector: str = 'General') -> Dict:
        """Comprehensive sentiment analysis combining multiple signals."""

        # Market regime sentiment
        market_sentiment = self._analyze_market_regime(technical_data)

        # Technical sentiment
        tech_sentiment = self._analyze_technical_sentiment(technical_data)

        # Pattern sentiment from candlesticks
        pattern_sentiment = self._analyze_pattern_sentiment(candlestick_data)

        # Volume sentiment
        volume_sentiment = self._analyze_volume_sentiment(technical_data)

        # Momentum sentiment
        momentum_sentiment = self._analyze_momentum(technical_data)

        # Sector-specific sentiment
        sector_data = self.SECTOR_WEIGHTS.get(sector, self.SECTOR_WEIGHTS['General'])
        sector_sentiment = self._analyze_sector(sector_data, tech_sentiment)

        # Fear & Greed index proxy
        fear_greed = self._calculate_fear_greed(technical_data, candlestick_data)

        # Composite score
        weights = {
            'market': 0.15,
            'technical': 0.25,
            'pattern': 0.15,
            'volume': 0.10,
            'momentum': 0.20,
            'sector': 0.15
        }

        composite = (
            market_sentiment['score'] * weights['market'] +
            tech_sentiment['score'] * weights['technical'] +
            pattern_sentiment['score'] * weights['pattern'] +
            volume_sentiment['score'] * weights['volume'] +
            momentum_sentiment['score'] * weights['momentum'] +
            sector_sentiment['score'] * weights['sector']
        )

        if composite > 65:
            overall = 'VERY_BULLISH'
            emoji = '🚀'
        elif composite > 55:
            overall = 'BULLISH'
            emoji = '📈'
        elif composite > 45:
            overall = 'NEUTRAL'
            emoji = '➡️'
        elif composite > 35:
            overall = 'BEARISH'
            emoji = '📉'
        else:
            overall = 'VERY_BEARISH'
            emoji = '💥'

        return {
            'overall': overall,
            'emoji': emoji,
            'composite_score': round(composite, 1),
            'fear_greed_index': fear_greed,
            'components': {
                'market_regime': market_sentiment,
                'technical': tech_sentiment,
                'patterns': pattern_sentiment,
                'volume': volume_sentiment,
                'momentum': momentum_sentiment,
                'sector': sector_sentiment
            },
            'recommendation': self._generate_recommendation(composite, fear_greed, technical_data)
        }

    def _analyze_market_regime(self, technical: Dict) -> Dict:
        """Determine current market regime."""
        score = 50

        # ADX trend strength
        adx = technical.get('adx', {})
        if adx.get('trend') == 'VERY_STRONG':
            if adx.get('direction') == 'BULLISH':
                score += 15
            else:
                score -= 15
        elif adx.get('trend') == 'STRONG':
            if adx.get('direction') == 'BULLISH':
                score += 10
            else:
                score -= 10

        # Moving average position
        ma = technical.get('moving_averages', {})
        if 'SMA_50' in ma and 'SMA_200' in ma:
            if ma.get('cross_signal', '').startswith('GOLDEN'):
                score += 12
            elif ma.get('cross_signal', '').startswith('DEATH'):
                score -= 12

        # Price vs SMAs
        for period in [20, 50, 200]:
            key = f'SMA_{period}_signal'
            if key in ma:
                score += 3 if ma[key] == 'BULLISH' else -3

        score = max(0, min(100, score))

        if score > 60:
            regime = 'BULL_MARKET'
        elif score < 40:
            regime = 'BEAR_MARKET'
        else:
            regime = 'SIDEWAYS'

        return {'score': score, 'regime': regime}

    def _analyze_technical_sentiment(self, technical: Dict) -> Dict:
        """Analyze sentiment from technical indicators."""
        score = 50
        signals = []

        # RSI
        rsi = technical.get('rsi', {})
        rsi_val = rsi.get('value', 50)
        if rsi_val > 60:
            score += 8
            signals.append(f'RSI bullish at {rsi_val}')
        elif rsi_val < 40:
            score -= 8
            signals.append(f'RSI bearish at {rsi_val}')
        if rsi_val < 30:
            score += 5  # Contrarian buy signal
            signals.append('RSI oversold - potential reversal')
        elif rsi_val > 70:
            score -= 5  # Contrarian sell signal
            signals.append('RSI overbought - potential reversal')

        # MACD
        macd = technical.get('macd', {})
        macd_sig = macd.get('signal_type', 'NEUTRAL')
        if 'BULLISH' in macd_sig:
            score += 10 if 'CROSSOVER' in macd_sig else 5
            signals.append(f'MACD {macd_sig}')
        elif 'BEARISH' in macd_sig:
            score -= 10 if 'CROSSOVER' in macd_sig else 5
            signals.append(f'MACD {macd_sig}')

        # Bollinger
        bb = technical.get('bollinger_bands', {})
        if bb.get('signal') == 'OVERSOLD':
            score += 5
            signals.append('Bollinger oversold')
        elif bb.get('signal') == 'OVERBOUGHT':
            score -= 5
            signals.append('Bollinger overbought')

        score = max(0, min(100, score))
        return {'score': score, 'signals': signals}

    def _analyze_pattern_sentiment(self, candlestick: Dict) -> Dict:
        """Analyze candlestick pattern sentiment."""
        score = 50

        bull_score = candlestick.get('bullish_score', 50)
        bear_score = candlestick.get('bearish_score', 50)

        score = 50 + (bull_score - bear_score) / 2

        recent = candlestick.get('recent_patterns', [])
        for p in recent[-5:]:
            if p['type'] == 'bullish':
                score += p['strength'] * 8
            elif p['type'] == 'bearish':
                score -= p['strength'] * 8

        score = max(0, min(100, score))

        top_patterns = []
        for p in recent:
            top_patterns.append(f"{p['pattern']} ({p['type']})")

        return {
            'score': score,
            'signal': candlestick.get('signal', 'NEUTRAL'),
            'recent_patterns': list(set(top_patterns))[:5]
        }

    def _analyze_volume_sentiment(self, technical: Dict) -> Dict:
        """Volume-based sentiment."""
        score = 50

        vol = technical.get('volume_analysis', {})
        ratio = vol.get('ratio', 1)

        if ratio > 2:
            score += 15  # High volume = conviction
        elif ratio > 1.5:
            score += 8
        elif ratio < 0.5:
            score -= 5

        # OBV
        obv = technical.get('obv', {})
        if obv.get('signal') == 'BULLISH':
            score += 8
        else:
            score -= 8

        # MFI
        mfi = technical.get('mfi', {})
        mfi_val = mfi.get('value', 50)
        if mfi_val > 80:
            score -= 5
        elif mfi_val < 20:
            score += 5

        # VWAP
        vwap = technical.get('vwap', {})
        if vwap.get('signal') == 'BULLISH':
            score += 5
        else:
            score -= 5

        score = max(0, min(100, score))
        return {'score': score, 'volume_signal': vol.get('signal', 'NORMAL'), 'volume_trend': vol.get('trend', 'NORMAL')}

    def _analyze_momentum(self, technical: Dict) -> Dict:
        """Momentum analysis."""
        score = 50

        # ROC
        roc = technical.get('roc', {})
        roc_val = roc.get('value', 0)
        if roc_val > 5:
            score += 15
        elif roc_val > 2:
            score += 10
        elif roc_val > 0:
            score += 5
        elif roc_val > -2:
            score -= 5
        elif roc_val > -5:
            score -= 10
        else:
            score -= 15

        # Williams %R
        wr = technical.get('williams_r', {})
        if wr.get('signal') == 'OVERSOLD':
            score += 5
        elif wr.get('signal') == 'OVERBOUGHT':
            score -= 5

        # CCI
        cci = technical.get('cci', {})
        if cci.get('signal') == 'OVERSOLD':
            score += 5
        elif cci.get('signal') == 'OVERBOUGHT':
            score -= 5

        # Stochastic
        stoch = technical.get('stochastic', {})
        if stoch.get('signal') == 'OVERSOLD':
            score += 5
        elif stoch.get('signal') == 'OVERBOUGHT':
            score -= 5

        score = max(0, min(100, score))
        return {'score': score, 'roc': roc_val}

    def _analyze_sector(self, sector_data: Dict, tech_sentiment: Dict) -> Dict:
        """Sector-specific analysis."""
        base_score = tech_sentiment['score']
        growth = sector_data['growth_factor']
        stability = sector_data['stability']

        adjusted = base_score * growth * stability
        score = max(0, min(100, adjusted))

        return {'score': score, 'growth_factor': growth, 'stability': stability}

    def _calculate_fear_greed(self, technical: Dict, candlestick: Dict) -> Dict:
        """Calculate Fear & Greed Index (0-100)."""
        components = []

        # Market momentum
        rsi = technical.get('rsi', {}).get('value', 50)
        components.append(rsi)

        # Trend strength
        adx = technical.get('adx', {})
        adx_val = adx.get('value', 25)
        adx_score = min(adx_val * 2, 100)
        if adx.get('direction') == 'BEARISH':
            adx_score = 100 - adx_score
        components.append(adx_score)

        # Pattern sentiment
        bull = candlestick.get('bullish_score', 50)
        bear = candlestick.get('bearish_score', 50)
        components.append(bull if bull > bear else 100 - bear)

        # Volume
        vol = technical.get('volume_analysis', {})
        vol_score = 50
        if vol.get('signal') == 'HIGH_VOLUME':
            vol_score = 70 if vol.get('trend') == 'INCREASING' else 30
        components.append(vol_score)

        # Stochastic
        stoch = technical.get('stochastic', {}).get('k', 50)
        components.append(stoch)

        # Bollinger position
        bb_pos = technical.get('bollinger_bands', {}).get('price_position', 50)
        components.append(bb_pos)

        index = np.mean(components)

        if index > 80:
            zone = 'EXTREME_GREED'
            warning = 'Market may be overheated. Consider taking profits.'
        elif index > 60:
            zone = 'GREED'
            warning = 'Market showing greed. Be cautious with new entries.'
        elif index > 40:
            zone = 'NEUTRAL'
            warning = 'Market is balanced. Good for selective stock picking.'
        elif index > 20:
            zone = 'FEAR'
            warning = 'Market showing fear. Good buying opportunities may arise.'
        else:
            zone = 'EXTREME_FEAR'
            warning = 'Extreme fear in market. Historically great buying opportunity.'

        return {
            'index': round(float(index), 1),
            'zone': zone,
            'warning': warning
        }

    def _generate_recommendation(self, composite: float, fear_greed: Dict, technical: Dict) -> Dict:
        """Generate actionable recommendation."""
        fg_idx = fear_greed['index']

        if composite > 65 and fg_idx < 70:
            action = 'AGGRESSIVE_BUY'
            message = 'Strong bullish signals across multiple indicators. Consider building position.'
            position_pct = 80
        elif composite > 55 and fg_idx < 60:
            action = 'BUY'
            message = 'Moderately bullish. Good entry point for quality stocks.'
            position_pct = 60
        elif composite > 45:
            action = 'HOLD_ACCUMULATE'
            message = 'Market is neutral. Accumulate on dips. Wait for clearer signals.'
            position_pct = 40
        elif composite > 35:
            action = 'HOLD_REDUCE'
            message = 'Bearish signals emerging. Consider reducing exposure.'
            position_pct = 25
        else:
            action = 'SELL_EXIT'
            message = 'Strong bearish signals. Consider exiting positions or strict stop-losses.'
            position_pct = 10

        # Contrarian adjustment
        if fg_idx < 20 and composite > 40:
            action = 'CONTRARIAN_BUY'
            message = 'Extreme fear presents rare buying opportunity. Selective buying recommended.'
            position_pct = 50

        return {
            'action': action,
            'message': message,
            'suggested_position_pct': position_pct
        }