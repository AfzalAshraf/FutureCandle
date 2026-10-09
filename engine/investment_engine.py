"""
Investment Recommendation Engine
Long-term investment strategy generator for Indian stock market
"""
import numpy as np
from typing import Dict, List
from datetime import datetime, timedelta


class InvestmentEngine:
    """
    Generates detailed investment recommendations for Indian stock market.
    Combines technical analysis, sentiment, and fundamental growth projections.
    """

    # Indian market historical returns by sector (annualized %)
    SECTOR_GROWTH_RATES = {
        'IT': {'conservative': 12, 'moderate': 16, 'aggressive': 22},
        'Banking': {'conservative': 10, 'moderate': 14, 'aggressive': 20},
        'Pharma': {'conservative': 11, 'moderate': 15, 'aggressive': 21},
        'FMCG': {'conservative': 10, 'moderate': 13, 'aggressive': 17},
        'Auto': {'conservative': 11, 'moderate': 16, 'aggressive': 24},
        'Energy': {'conservative': 9, 'moderate': 14, 'aggressive': 22},
        'Metals': {'conservative': 8, 'moderate': 14, 'aggressive': 25},
        'Realty': {'conservative': 10, 'moderate': 17, 'aggressive': 28},
        'Infra': {'conservative': 10, 'moderate': 15, 'aggressive': 23},
        'Defense': {'conservative': 12, 'moderate': 18, 'aggressive': 26},
        'Cement': {'conservative': 9, 'moderate': 13, 'aggressive': 19},
        'Telecom': {'conservative': 8, 'moderate': 14, 'aggressive': 22},
        'General': {'conservative': 10, 'moderate': 14, 'aggressive': 20}
    }

    # Indian market risk-free rate (10Y Gov Bond)
    RISK_FREE_RATE = 7.0

    # Market cap categories
    MARKET_CAP_CATEGORIES = {
        'Large Cap': {'min': 20000, 'risk': 0.6, 'return_mult': 0.9},
        'Mid Cap': {'min': 5000, 'risk': 0.8, 'return_mult': 1.1},
        'Small Cap': {'min': 500, 'risk': 1.0, 'return_mult': 1.3},
        'Micro Cap': {'min': 0, 'risk': 1.3, 'return_mult': 1.6}
    }

    def generate_recommendation(self, symbol: str, current_price: float,
                                technical: Dict, sentiment: Dict,
                                candlestick: Dict, sector: str = 'General',
                                market_cap_cr: float = 20000) -> Dict:
        """Generate comprehensive investment recommendation."""

        # Determine market cap category
        cap_category = 'Large Cap'
        for cat, data in sorted(self.MARKET_CAP_CATEGORIES.items(), key=lambda x: -x[1]['min']):
            if market_cap_cr >= data['min']:
                cap_category = cat
                break

        cap_data = self.MARKET_CAP_CATEGORIES[cap_category]

        # Get sector growth rates
        growth_rates = self.SECTOR_GROWTH_RATES.get(sector, self.SECTOR_GROWTH_RATES['General'])

        # Technical signal strength
        tech_score = technical.get('overall_score', 50)
        tech_signal = technical.get('signal', {})
        sentiment_score = sentiment.get('composite_score', 50)
        fear_greed = sentiment.get('fear_greed_index', {}).get('index', 50)

        # Calculate risk profile
        risk_profile = self._calculate_risk(technical, sentiment, cap_data)

        # Generate price targets
        price_targets = self._calculate_price_targets(
            current_price, growth_rates, cap_data, tech_score, sentiment_score, risk_profile
        )

        # Investment strategy
        strategy = self._generate_strategy(
            tech_score, sentiment_score, fear_greed, risk_profile, cap_category, growth_rates
        )

        # Portfolio allocation
        allocation = self._calculate_allocation(strategy, risk_profile, cap_category)

        # Entry/Exit points
        entry_exit = self._calculate_entry_exit(technical, current_price)

        # Compounding projections
        projections = self._calculate_projections(current_price, growth_rates, strategy)

        # Investment duration recommendation
        duration = self._recommend_duration(strategy, risk_profile, growth_rates, cap_category)

        # SIP recommendations
        sip = self._sip_recommendation(strategy, current_price, duration)

        # Risk warnings
        risks = self._assess_risks(technical, sentiment, candlestick, sector, cap_category)

        # Final verdict
        verdict = self._generate_verdict(
            strategy, price_targets, duration, risk_profile, tech_score, sentiment_score
        )

        return {
            'symbol': symbol,
            'current_price': current_price,
            'sector': sector,
            'market_cap_category': cap_category,
            'market_cap_cr': market_cap_cr,
            'risk_profile': risk_profile,
            'price_targets': price_targets,
            'strategy': strategy,
            'allocation': allocation,
            'entry_exit': entry_exit,
            'projections': projections,
            'duration': duration,
            'sip': sip,
            'risks': risks,
            'verdict': verdict
        }

    def _calculate_risk(self, technical: Dict, sentiment: Dict, cap_data: Dict) -> Dict:
        """Calculate comprehensive risk profile."""
        atr = technical.get('atr', {})
        atr_pct = atr.get('percentage', 2.0)
        volatility = atr.get('volatility', 'MODERATE')

        # ADX trend stability
        adx = technical.get('adx', {})
        trend = adx.get('trend', 'WEAK')
        trend_risk = {'VERY_STRONG': 0.3, 'STRONG': 0.4, 'MODERATE': 0.6, 'WEAK': 0.8}.get(trend, 0.5)

        # Bollinger bandwidth
        bb = technical.get('bollinger_bands', {})
        bandwidth = bb.get('bandwidth', 5)

        # Base risk from market cap
        base_risk = cap_data['risk']

        # Composite risk score (0-100, lower is safer)
        risk_score = (
            min(atr_pct * 10, 30) +  # Volatility component (max 30)
            trend_risk * 25 +          # Trend stability (max 25)
            min(bandwidth * 2, 20) +   # Price volatility (max 20)
            base_risk * 25             # Market cap risk (max 25)
        )

        risk_score = min(100, max(0, risk_score))

        if risk_score < 30:
            level = 'LOW'
            color = 'green'
        elif risk_score < 50:
            level = 'MODERATE'
            color = 'yellow'
        elif risk_score < 70:
            level = 'HIGH'
            color = 'orange'
        else:
            level = 'VERY_HIGH'
            color = 'red'

        return {
            'score': round(risk_score, 1),
            'level': level,
            'color': color,
            'volatility': volatility,
            'atr_percentage': atr_pct,
            'trend_stability': trend,
            'components': {
                'volatility_risk': round(min(atr_pct * 10, 30), 1),
                'trend_risk': round(trend_risk * 25, 1),
                'price_volatility': round(min(bandwidth * 2, 20), 1),
                'cap_risk': round(base_risk * 25, 1)
            }
        }

    def _calculate_price_targets(self, price: float, growth_rates: Dict,
                                 cap_data: Dict, tech_score: float,
                                 sentiment_score: float, risk: Dict) -> Dict:
        """Calculate price targets for different timeframes."""
        mult = cap_data['return_mult']

        # Adjust growth based on current signals
        signal_adj = (tech_score + sentiment_score) / 200  # 0 to 1
        adj_factor = 0.7 + signal_adj * 0.6  # 0.7 to 1.3

        targets = {}
        for scenario in ['conservative', 'moderate', 'aggressive']:
            annual_rate = growth_rates[scenario] * mult * adj_factor / 100
            targets[scenario] = {}
            for years in [1, 2, 3, 5, 7, 10, 15, 20]:
                targets[scenario][f'{years}Y'] = {
                    'price': round(price * (1 + annual_rate) ** years, 2),
                    'return_pct': round(((1 + annual_rate) ** years - 1) * 100, 1),
                    'cagr': round(annual_rate * 100, 1)
                }

        # Near-term targets (3-6 months)
        atr = risk.get('atr_percentage', 2)
        near_term = {
            '3_month_bull': round(price * (1 + atr * 3 / 100), 2),
            '3_month_bear': round(price * (1 - atr * 3 / 100), 2),
            '6_month_bull': round(price * (1 + atr * 5 / 100), 2),
            '6_month_bear': round(price * (1 - atr * 4 / 100), 2),
            '1_year_bull': round(price * 1.3, 2),
            '1_year_bear': round(price * 0.8, 2)
        }

        targets['near_term'] = near_term

        return targets

    def _generate_strategy(self, tech_score: float, sentiment_score: float,
                           fear_greed: float, risk: Dict, cap_cat: str,
                           growth_rates: Dict) -> Dict:
        """Generate investment strategy."""

        combined = (tech_score + sentiment_score) / 2

        if combined > 65 and fear_greed < 70:
            strategy_type = 'AGGRESSIVE_GROWTH'
            description = 'Strong bullish convergence across indicators. Ideal for growth-focused portfolio.'
            risk_appetite = 'HIGH'
        elif combined > 55:
            strategy_type = 'GROWTH'
            description = 'Moderately bullish outlook. Balanced growth approach recommended.'
            risk_appetite = 'MODERATE_HIGH'
        elif combined > 45:
            strategy_type = 'BALANCED'
            description = 'Neutral market conditions. Mix of growth and stability.'
            risk_appetite = 'MODERATE'
        elif combined > 35:
            strategy_type = 'DEFENSIVE'
            description = 'Bearish signals emerging. Focus on defensive stocks and stability.'
            risk_appetite = 'LOW_MODERATE'
        else:
            strategy_type = 'CAPITAL_PRESERVATION'
            description = 'Strong bearish signals. Capital preservation is priority.'
            risk_appetite = 'LOW'

        # SIP vs Lumpsum
        if risk['score'] > 50:
            investment_mode = 'SIP (Systematic Investment Plan)'
            mode_reason = 'High volatility makes SIP ideal to average out costs.'
        elif risk['score'] > 30:
            investment_mode = 'SIP + Partial Lumpsum'
            mode_reason = 'Moderate risk. Combine SIP with strategic lumpsum on dips.'
        else:
            investment_mode = 'Lumpsum + SIP'
            mode_reason = 'Low risk environment. Good for lumpsum with SIP backbone.'

        return {
            'type': strategy_type,
            'description': description,
            'risk_appetite': risk_appetite,
            'investment_mode': investment_mode,
            'mode_reason': mode_reason,
            'combined_score': round(combined, 1)
        }

    def _calculate_allocation(self, strategy: Dict, risk: Dict, cap_cat: str) -> Dict:
        """Calculate portfolio allocation recommendations."""

        strat_type = strategy['type']

        allocations = {
            'AGGRESSIVE_GROWTH': {
                'equity': 80, 'debt': 10, 'gold': 5, 'cash': 5,
                'large_cap': 30, 'mid_cap': 35, 'small_cap': 25, 'micro_cap': 10
            },
            'GROWTH': {
                'equity': 70, 'debt': 15, 'gold': 10, 'cash': 5,
                'large_cap': 40, 'mid_cap': 30, 'small_cap': 20, 'micro_cap': 10
            },
            'BALANCED': {
                'equity': 55, 'debt': 25, 'gold': 12, 'cash': 8,
                'large_cap': 50, 'mid_cap': 30, 'small_cap': 15, 'micro_cap': 5
            },
            'DEFENSIVE': {
                'equity': 35, 'debt': 35, 'gold': 18, 'cash': 12,
                'large_cap': 65, 'mid_cap': 25, 'small_cap': 10, 'micro_cap': 0
            },
            'CAPITAL_PRESERVATION': {
                'equity': 20, 'debt': 45, 'gold': 20, 'cash': 15,
                'large_cap': 80, 'mid_cap': 15, 'small_cap': 5, 'micro_cap': 0
            }
        }

        alloc = allocations.get(strat_type, allocations['BALANCED'])

        # Sector allocation suggestion
        sector_alloc = self._sector_allocation(strategy, risk)

        return {
            'asset_allocation': alloc,
            'cap_allocation': {
                'large_cap': alloc['large_cap'],
                'mid_cap': alloc['mid_cap'],
                'small_cap': alloc['small_cap'],
                'micro_cap': alloc['micro_cap']
            },
            'sector_suggestions': sector_alloc
        }

    def _sector_allocation(self, strategy: Dict, risk: Dict) -> List[Dict]:
        """Suggest sector allocation."""
        sectors = []

        strat = strategy['type']
        if strat in ['AGGRESSIVE_GROWTH', 'GROWTH']:
            sectors = [
                {'sector': 'IT', 'weight': 20, 'reason': 'Digital transformation, global demand'},
                {'sector': 'Banking', 'weight': 18, 'reason': 'Credit growth, economic recovery'},
                {'sector': 'Defense', 'weight': 15, 'reason': 'Government spending, Make in India'},
                {'sector': 'Infra', 'weight': 15, 'reason': 'National Infrastructure Pipeline'},
                {'sector': 'Auto', 'weight': 12, 'reason': 'EV transition, demand recovery'},
                {'sector': 'Pharma', 'weight': 10, 'reason': 'Healthcare spending, exports'},
                {'sector': 'Energy', 'weight': 10, 'reason': 'Green energy transition'}
            ]
        elif strat == 'BALANCED':
            sectors = [
                {'sector': 'FMCG', 'weight': 20, 'reason': 'Stable demand, consistent growth'},
                {'sector': 'IT', 'weight': 18, 'reason': 'Quality earnings, dividends'},
                {'sector': 'Banking', 'weight': 18, 'reason': 'Systemic importance'},
                {'sector': 'Pharma', 'weight': 15, 'reason': 'Defensive with growth'},
                {'sector': 'Infra', 'weight': 12, 'reason': 'Government push'},
                {'sector': 'Auto', 'weight': 10, 'reason': 'Cyclical recovery'},
                {'sector': 'Cement', 'weight': 7, 'reason': 'Construction demand'}
            ]
        else:
            sectors = [
                {'sector': 'FMCG', 'weight': 25, 'reason': 'Recession-proof demand'},
                {'sector': 'Pharma', 'weight': 22, 'reason': 'Essential services'},
                {'sector': 'IT', 'weight': 20, 'reason': 'Dollar revenue hedge'},
                {'sector': 'Banking', 'weight': 15, 'reason': 'Dividend yields'},
                {'sector': 'Cement', 'weight': 10, 'reason': 'Stable demand'},
                {'sector': 'Energy', 'weight': 8, 'reason': 'Essential services'}
            ]

        return sectors

    def _calculate_entry_exit(self, technical: Dict, current_price: float) -> Dict:
        """Calculate entry and exit points."""
        sr = technical.get('support_resistance', {})
        pivot = technical.get('pivot_points', {})
        fib = technical.get('fibonacci', {})
        bb = technical.get('bollinger_bands', {})

        # Entry zones
        support1 = sr.get('nearest_support', current_price * 0.97)
        support2 = pivot.get('s2', current_price * 0.95)
        bb_lower = bb.get('lower', current_price * 0.96)

        # Exit/target zones
        resistance1 = sr.get('nearest_resistance', current_price * 1.03)
        resistance2 = pivot.get('r2', current_price * 1.05)
        bb_upper = bb.get('upper', current_price * 1.04)

        # Stop loss
        stop_loss = round(min(support1, bb_lower) * 0.98, 2)
        stop_loss_pct = round((current_price - stop_loss) / current_price * 100, 1)

        return {
            'ideal_entry': round((support1 + current_price) / 2, 2),
            'aggressive_entry': round(current_price, 2),
            'conservative_entry': round(support1, 2),
            'buy_on_dip': round(bb_lower, 2),
            'target_1': round(resistance1, 2),
            'target_2': round(resistance2, 2),
            'target_3': round(bb_upper * 1.02, 2),
            'stop_loss': stop_loss,
            'stop_loss_pct': stop_loss_pct,
            'risk_reward_ratio': round((resistance1 - current_price) / (current_price - stop_loss), 2) if current_price > stop_loss else 0,
            'supports': [round(support1, 2), round(support2, 2)],
            'resistances': [round(resistance1, 2), round(resistance2, 2)]
        }

    def _calculate_projections(self, price: float, growth_rates: Dict, strategy: Dict) -> Dict:
        """Calculate wealth creation projections for different investment amounts."""
        strat_type = strategy['type']

        if strat_type in ['AGGRESSIVE_GROWTH', 'GROWTH']:
            rate = growth_rates['moderate']
        elif strat_type == 'BALANCED':
            rate = (growth_rates['conservative'] + growth_rates['moderate']) / 2
        else:
            rate = growth_rates['conservative']

        amounts = [10000, 25000, 50000, 100000, 250000, 500000, 1000000, 5000000]
        projections = {}

        for amount in amounts:
            key = f'₹{amount:,}'
            projections[key] = {}
            for years in [1, 3, 5, 7, 10, 15, 20, 25]:
                future_value = amount * (1 + rate/100) ** years
                profit = future_value - amount
                mult = future_value / amount
                projections[key][f'{years}Y'] = {
                    'invested': amount,
                    'future_value': round(future_value, 0),
                    'profit': round(profit, 0),
                    'multiplier': round(mult, 2),
                    'cagr': rate
                }

        # SIP projections
        sip_projections = {}
        for sip_amount in [1000, 2000, 5000, 10000, 25000, 50000]:
            key = f'₹{sip_amount:,}/month'
            sip_projections[key] = {}
            monthly_rate = rate / 12 / 100
            for years in [3, 5, 7, 10, 15, 20, 25]:
                months = years * 12
                # SIP future value formula
                if monthly_rate > 0:
                    fv = sip_amount * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
                else:
                    fv = sip_amount * months
                invested = sip_amount * months
                profit = fv - invested

                sip_projections[key][f'{years}Y'] = {
                    'total_invested': round(invested, 0),
                    'future_value': round(fv, 0),
                    'profit': round(profit, 0),
                    'multiplier': round(fv / invested, 2) if invested > 0 else 0,
                    'cagr': rate
                }

        return {
            'lumpsum': projections,
            'sip': sip_projections
        }

    def _recommend_duration(self, strategy: Dict, risk: Dict,
                            growth_rates: Dict, cap_cat: str) -> Dict:
        """Recommend investment duration."""
        strat = strategy['type']

        durations = {
            'AGGRESSIVE_GROWTH': {
                'minimum': '3 years',
                'recommended': '5-7 years',
                'optimal': '10+ years',
                'min_years': 3,
                'rec_years': 7,
                'opt_years': 15,
                'reason': 'Aggressive growth stocks need time to compound. Minimum 3 years to ride out volatility.'
            },
            'GROWTH': {
                'minimum': '2 years',
                'recommended': '5-7 years',
                'optimal': '10+ years',
                'min_years': 2,
                'rec_years': 5,
                'opt_years': 10,
                'reason': 'Growth stocks benefit from 5+ year holding. Short-term may show volatility.'
            },
            'BALANCED': {
                'minimum': '2 years',
                'recommended': '3-5 years',
                'optimal': '7-10 years',
                'min_years': 2,
                'rec_years': 5,
                'opt_years': 7,
                'reason': 'Balanced portfolio works well for 3-7 year horizon with moderate returns.'
            },
            'DEFENSIVE': {
                'minimum': '1 year',
                'recommended': '2-3 years',
                'optimal': '5-7 years',
                'min_years': 1,
                'rec_years': 3,
                'opt_years': 5,
                'reason': 'Defensive stocks offer stability. 2-5 years for meaningful returns.'
            },
            'CAPITAL_PRESERVATION': {
                'minimum': '6 months',
                'recommended': '1-2 years',
                'optimal': '3-5 years',
                'min_years': 1,
                'rec_years': 2,
                'opt_years': 3,
                'reason': 'Focus on capital safety. Short to medium term with debt-heavy allocation.'
            }
        }

        dur = durations.get(strat, durations['BALANCED'])

        # Add market cycle context
        dur['market_cycle'] = 'Indian market typically goes through 3-5 year cycles. Current phase analysis suggests {} years as ideal.'.format(dur['rec_years'])

        # Tax implications (India)
        dur['tax_note'] = ('LTCG (Long Term Capital Gain) on equity: 10% above ₹1 lakh after 1 year. '
                          'STCG (Short Term): 15%. Holding for 1+ year saves tax. '
                          'ELSS mutual funds: 3-year lock-in with 80C deduction.')

        return dur

    def _sip_recommendation(self, strategy: Dict, price: float, duration: Dict) -> Dict:
        """Generate SIP recommendations."""
        strat = strategy['type']
        rec_years = duration.get('rec_years', 5)

        if strat in ['AGGRESSIVE_GROWTH', 'GROWTH']:
            sip_pct = 30  # % of monthly income
            sip_frequency = 'Monthly'
        elif strat == 'BALANCED':
            sip_pct = 20
            sip_frequency = 'Monthly'
        else:
            sip_pct = 15
            sip_frequency = 'Monthly/Bi-monthly'

        # Minimum SIP based on stock price
        if price > 5000:
            min_sip = 'Consider ETF/Index fund for diversification'
            min_shares = 1
        elif price > 1000:
            min_sip = f'Minimum 1 share = ₹{price:,.0f}'
            min_shares = 1
        else:
            min_sip = f'Minimum lot: ₹{price * 10:,.0f} (10 shares)'
            min_shares = 10

        # Step-up SIP recommendation
        step_up = {
            'year_1': 'Base SIP amount',
            'year_2': 'Increase by 10-15%',
            'year_3': 'Increase by 10-15%',
            'year_5': 'Review and rebalance',
            'note': 'Step-up SIP (increasing SIP by 10% annually) generates 20-30% more wealth than flat SIP.'
        }

        return {
            'recommended_frequency': sip_frequency,
            'income_allocation_pct': sip_pct,
            'minimum_investment': min_sip,
            'step_up': step_up,
            'duration': f'{rec_years} years',
            'auto_invest': 'Enable auto-debit for discipline',
            'best_day': 'SIP on 1st or 5th of month (historically better entry)',
            'platforms': ['Zerodha (Kite)', 'Groww', 'Upstox', 'Angel One', 'ICICI Direct', 'HDFC Securities']
        }

    def _assess_risks(self, technical: Dict, sentiment: Dict,
                      candlestick: Dict, sector: str, cap_cat: str) -> Dict:
        """Comprehensive risk assessment."""
        risks = []

        # Technical risks
        rsi = technical.get('rsi', {}).get('value', 50)
        if rsi > 70:
            risks.append({'level': 'HIGH', 'type': 'Overbought Risk', 'detail': f'RSI at {rsi} - stock may be overbought'})
        if rsi < 30:
            risks.append({'level': 'MEDIUM', 'type': 'Oversold Risk', 'detail': f'RSI at {rsi} - may indicate fundamental issues'})

        # Volatility risk
        atr = technical.get('atr', {})
        if atr.get('volatility') in ['HIGH', 'VERY_HIGH']:
            risks.append({'level': 'HIGH', 'type': 'Volatility Risk', 'detail': f'High volatility ({atr.get("percentage", 0):.1f}% ATR). Use stop-losses.'})

        # Trend risk
        trend = technical.get('trend_strength', {})
        if trend.get('direction') in ['BEARISH', 'STRONG_BEARISH']:
            risks.append({'level': 'HIGH', 'type': 'Trend Risk', 'detail': 'Bearish trend detected. Price may continue declining.'})

        # Volume risk
        vol = technical.get('volume_analysis', {})
        if vol.get('signal') == 'LOW_VOLUME':
            risks.append({'level': 'MEDIUM', 'type': 'Liquidity Risk', 'detail': 'Low volume may cause slippage in large orders'})

        # Cap-specific risks
        cap_risks = {
            'Large Cap': 'Lower risk but potentially lower returns. Good for stability.',
            'Mid Cap': 'Moderate risk. Can outperform in bull markets, underperform in bears.',
            'Small Cap': 'High risk, high reward. Significant drawdown possible. 5+ year horizon recommended.',
            'Micro Cap': 'Very high risk. Illiquid. Only for experienced investors with high risk tolerance.'
        }
        risks.append({'level': 'INFO', 'type': 'Cap Risk', 'detail': cap_risks.get(cap_cat, '')})

        # Sector risks
        sector_risk_map = {
            'IT': 'US recession risk, H1B visa policy, forex fluctuation',
            'Banking': 'NPA risk, interest rate changes, regulatory changes',
            'Pharma': 'US FDA observations, drug pricing pressure, patent cliffs',
            'Auto': 'EV disruption, semiconductor shortage, commodity prices',
            'Metals': 'Global commodity cycles, China demand, carbon regulations',
            'Realty': 'Interest rate sensitivity, regulatory changes, liquidity risk',
            'Energy': 'Crude oil prices, green transition, subsidy changes',
            'Defense': 'Government budget cycles, geopolitical tensions',
            'FMCG': 'Rural demand, input cost inflation, competition',
            'Infra': 'Execution risk, policy changes, interest rate sensitivity'
        }
        if sector in sector_risk_map:
            risks.append({'level': 'MEDIUM', 'type': 'Sector Risk', 'detail': sector_risk_map[sector]})

        # General market risks
        risks.extend([
            {'level': 'MEDIUM', 'type': 'Market Risk', 'detail': 'Systematic risk affects all stocks. Diversify across sectors.'},
            {'level': 'LOW', 'type': 'Inflation Risk', 'detail': 'Indian inflation can erode real returns. Equity historically beats inflation.'},
            {'level': 'LOW', 'type': 'Currency Risk', 'detail': 'INR depreciation affects import costs but benefits export-oriented companies.'},
            {'level': 'INFO', 'type': 'Regulatory Risk', 'detail': 'SEBI regulations, tax policy changes, FPI rules can impact markets.'}
        ])

        # Risk score
        high_count = len([r for r in risks if r['level'] == 'HIGH'])
        med_count = len([r for r in risks if r['level'] == 'MEDIUM'])

        if high_count >= 3:
            overall_risk = 'VERY_HIGH'
        elif high_count >= 2:
            overall_risk = 'HIGH'
        elif high_count >= 1 or med_count >= 3:
            overall_risk = 'MODERATE'
        else:
            overall_risk = 'LOW'

        return {
            'individual_risks': risks,
            'overall_risk_level': overall_risk,
            'risk_count': {'high': high_count, 'medium': med_count, 'low': len([r for r in risks if r['level'] == 'LOW'])}
        }

    def _generate_verdict(self, strategy: Dict, price_targets: Dict,
                          duration: Dict, risk: Dict,
                          tech_score: float, sentiment_score: float) -> Dict:
        """Generate final investment verdict."""
        combined = (tech_score + sentiment_score) / 2
        strat = strategy['type']

        if combined > 65:
            verdict = 'STRONGLY RECOMMENDED FOR LONG-TERM INVESTMENT'
            stars = 5
        elif combined > 55:
            verdict = 'RECOMMENDED WITH CAUTION'
            stars = 4
        elif combined > 45:
            verdict = 'NEUTRAL - WAIT FOR BETTER ENTRY'
            stars = 3
        elif combined > 35:
            verdict = 'NOT RECOMMENDED - HIGH RISK'
            stars = 2
        else:
            verdict = 'AVOID - BEARISH OUTLOOK'
            stars = 1

        # Best time to invest
        if risk['score'] < 40 and combined > 50:
            timing = 'NOW is a good time to start accumulating.'
        elif risk['score'] < 60 and combined > 45:
            timing = 'Start SIP now. Add lumpsum on dips.'
        else:
            timing = 'Wait for better entry. Start with small SIP.'

        # Long-term outlook
        mod_target = price_targets.get('moderate', {})
        target_5y = mod_target.get('5Y', {}).get('price', 0)
        target_10y = mod_target.get('10Y', {}).get('price', 0)
        cagr = mod_target.get('5Y', {}).get('cagr', 12)

        return {
            'verdict': verdict,
            'stars': stars,
            'timing': timing,
            'expected_cagr': f'{cagr}%',
            'target_5_year': f'₹{target_5y:,.2f}',
            'target_10_year': f'₹{target_10y:,.2f}',
            'recommended_duration': duration['recommended'],
            'ideal_amount': strategy.get('investment_mode', 'SIP'),
            'key_message': (f'{strategy["description"]} Invest for {duration["recommended"]} '
                          f'with expected CAGR of {cagr}%. {timing}'),
            'disclaimer': ('⚠️ DISCLAIMER: This is algorithmic analysis based on technical indicators and '
                          'historical patterns. This is NOT financial advice. Past performance does not '
                          'guarantee future results. Always consult a SEBI-registered financial advisor '
                          'before making investment decisions. Stock market investments carry inherent risks.')
        }