"""
Indian Stock Market Indices — Complete Reference
All major NSE + BSE indices with sector mapping
"""

INDIAN_INDICES = {
    # ===================== BROAD MARKET =====================
    "^NSEI": {
        "name": "Nifty 50",
        "exchange": "NSE",
        "category": "Broad Market",
        "sector": "General",
        "description": "Top 50 companies by market cap on NSE"
    },
    "^BSESN": {
        "name": "Sensex",
        "exchange": "BSE",
        "category": "Broad Market",
        "sector": "General",
        "description": "Top 30 companies on BSE"
    },
    "^NSEMDCP50": {
        "name": "Nifty Midcap 50",
        "exchange": "NSE",
        "category": "Broad Market",
        "sector": "General",
        "description": "Top 50 mid-cap companies"
    },
    "NIFTY_MIDCAP_100.NS": {
        "name": "Nifty Midcap 100",
        "exchange": "NSE",
        "category": "Broad Market",
        "sector": "General",
        "description": "Top 100 mid-cap companies"
    },
    "NIFTY_SMLCAP_100.NS": {
        "name": "Nifty Smallcap 100",
        "exchange": "NSE",
        "category": "Broad Market",
        "sector": "General",
        "description": "Top 100 small-cap companies"
    },
    "^NSMIDCP": {
        "name": "Nifty Next 50",
        "exchange": "NSE",
        "category": "Broad Market",
        "sector": "General",
        "description": "Next 50 companies after Nifty 50"
    },
    "^NSEMDCP150": {
        "name": "Nifty Midcap 150",
        "exchange": "NSE",
        "category": "Broad Market",
        "sector": "General",
        "description": "Top 150 mid-cap companies"
    },
    "NIFTY_TOTAL_MKT.NS": {
        "name": "Nifty Total Market",
        "exchange": "NSE",
        "category": "Broad Market",
        "sector": "General",
        "description": "750+ companies covering entire NSE market"
    },
    "NIFTY500.NS": {
        "name": "Nifty 500",
        "exchange": "NSE",
        "category": "Broad Market",
        "sector": "General",
        "description": "Top 500 companies representing 95%+ of market"
    },
    "NIFTY_MICROCAP_250.NS": {
        "name": "Nifty Microcap 250",
        "exchange": "NSE",
        "category": "Broad Market",
        "sector": "General",
        "description": "Top 250 micro-cap companies"
    },

    # ===================== SECTORAL INDICES =====================
    "^CNXIT": {
        "name": "Nifty IT",
        "exchange": "NSE",
        "category": "Sectoral",
        "sector": "IT",
        "description": "Top IT companies — TCS, Infosys, Wipro, HCL, TechM"
    },
    "^NSEBANK": {
        "name": "Nifty Bank",
        "exchange": "NSE",
        "category": "Sectoral",
        "sector": "Banking",
        "description": "Top banking stocks — HDFC Bank, ICICI, SBI, Kotak, Axis"
    },
    "NIFTY_PHARMA.NS": {
        "name": "Nifty Pharma",
        "exchange": "NSE",
        "category": "Sectoral",
        "sector": "Pharma",
        "description": "Top pharma companies — Sun Pharma, Dr Reddy's, Cipla"
    },
    "NIFTY_AUTO.NS": {
        "name": "Nifty Auto",
        "exchange": "NSE",
        "category": "Sectoral",
        "sector": "Auto",
        "description": "Auto sector — Maruti, Tata Motors, M&M, Hero, Bajaj"
    },
    "NIFTY_FMCG.NS": {
        "name": "Nifty FMCG",
        "exchange": "NSE",
        "category": "Sectoral",
        "sector": "FMCG",
        "description": "FMCG giants — HUL, ITC, Nestle, Britannia, Dabur"
    },
    "NIFTY_METAL.NS": {
        "name": "Nifty Metal",
        "exchange": "NSE",
        "category": "Sectoral",
        "sector": "Metals",
        "description": "Metal companies — Tata Steel, JSW, Hindalco, Coal India"
    },
    "NIFTY_ENERGY.NS": {
        "name": "Nifty Energy",
        "exchange": "NSE",
        "category": "Sectoral",
        "sector": "Energy",
        "description": "Energy sector — Reliance, ONGC, NTPC, Power Grid"
    },
    "NIFTY_REALTY.NS": {
        "name": "Nifty Realty",
        "exchange": "NSE",
        "category": "Sectoral",
        "sector": "Realty",
        "description": "Real estate — DLF, Godrej Properties, Prestige, Oberoi"
    },
    "NIFTY_INFRA.NS": {
        "name": "Nifty Infrastructure",
        "exchange": "NSE",
        "category": "Sectoral",
        "sector": "Infra",
        "description": "Infrastructure — L&T, Adani Ports, Bharti, Siemens"
    },
    "NIFTY_PVT_BANK.NS": {
        "name": "Nifty Private Bank",
        "exchange": "NSE",
        "category": "Sectoral",
        "sector": "Banking",
        "description": "Private banks — HDFC, ICICI, Kotak, Axis, IndusInd"
    },
    "NIFTY_PSU_BANK.NS": {
        "name": "Nifty PSU Bank",
        "exchange": "NSE",
        "category": "Sectoral",
        "sector": "Banking",
        "description": "Government banks — SBI, Bank of Baroda, PNB, Canara"
    },
    "NIFTY_MEDIA.NS": {
        "name": "Nifty Media",
        "exchange": "NSE",
        "category": "Sectoral",
        "sector": "Media",
        "description": "Media companies — Zee, Sun TV, PVR Inox, Nazara"
    },
    "NIFTY_consum.NS": {
        "name": "Nifty Consumption",
        "exchange": "NSE",
        "category": "Sectoral",
        "sector": "FMCG",
        "description": "Consumer-facing companies across sectors"
    },
    "NIFTY_COMMODITIES.NS": {
        "name": "Nifty Commodities",
        "exchange": "NSE",
        "category": "Sectoral",
        "sector": "Metals",
        "description": "Commodity companies — metals, mining, oil, gas"
    },
    "NIFTY_SERV_SECTOR.NS": {
        "name": "Nifty Services Sector",
        "exchange": "NSE",
        "category": "Sectoral",
        "sector": "IT",
        "description": "Service sector — IT, banking, financial services"
    },
    "NIFTY_MNC.NS": {
        "name": "Nifty MNC",
        "exchange": "NSE",
        "category": "Sectoral",
        "sector": "General",
        "description": "Multinational companies listed in India"
    },
    "NIFTY_INDIA_MFG.NS": {
        "name": "Nifty India Manufacturing",
        "exchange": "NSE",
        "category": "Sectoral",
        "sector": "Infra",
        "description": "Manufacturing companies under Make in India"
    },
    "NIFTY_INDIA_DIGITAL.NS": {
        "name": "Nifty India Digital",
        "exchange": "NSE",
        "category": "Sectoral",
        "sector": "IT",
        "description": "Digital/tech companies in India"
    },
    "NIFTY_HEALTHCARE.NS": {
        "name": "Nifty Healthcare",
        "exchange": "NSE",
        "category": "Sectoral",
        "sector": "Pharma",
        "description": "Healthcare — hospitals, pharma, diagnostics"
    },
    "NIFTY_OIL_GAS.NS": {
        "name": "Nifty Oil & Gas",
        "exchange": "NSE",
        "category": "Sectoral",
        "sector": "Energy",
        "description": "Oil & gas companies — Reliance, ONGC, GAIL, IOC"
    },
    "NIFTY_FIN_SERVICE.NS": {
        "name": "Nifty Financial Services",
        "exchange": "NSE",
        "category": "Sectoral",
        "sector": "Banking",
        "description": "Banks, NBFCs, insurance, housing finance"
    },
    "NIFTY_CPSE.NS": {
        "name": "Nifty CPSE",
        "exchange": "NSE",
        "category": "Sectoral",
        "sector": "Energy",
        "description": "Central Public Sector Enterprises"
    },
    "NIFTY_PSE.NS": {
        "name": "Nifty PSE",
        "exchange": "NSE",
        "category": "Sectoral",
        "sector": "Energy",
        "description": "Public Sector Enterprises"
    },

    # ===================== THEMATIC =====================
    "NIFTY_DEFENCE.NS": {
        "name": "Nifty Defence",
        "exchange": "NSE",
        "category": "Thematic",
        "sector": "Defense",
        "description": "Defence & aerospace — HAL, BEL, BDL, Solar Industries"
    },
    "NIFTY_EV_N_NEW_AUTOMOTIVE.NS": {
        "name": "Nifty EV & New Age Automotive",
        "exchange": "NSE",
        "category": "Thematic",
        "sector": "Auto",
        "description": "Electric vehicles and new-age auto companies"
    },
    "NIFTY_INDIA_RAILWAYS_NIPPON.NS": {
        "name": "Nifty India Railways",
        "exchange": "NSE",
        "category": "Thematic",
        "sector": "Infra",
        "description": "Railway-related companies — IRFC, RVNL, IRCTC, RITES"
    },
    "NIFTY_INDIA_TMSC.TI": {
        "name": "Nifty Tata Group",
        "exchange": "NSE",
        "category": "Thematic",
        "sector": "General",
        "description": "Tata Group companies"
    },
    "NIFTY500_MULTICAP.NS": {
        "name": "Nifty 500 Multicap",
        "exchange": "NSE",
        "category": "Thematic",
        "sector": "General",
        "description": "Multicap representation of Nifty 500"
    },
    "NIFTY_GROWSECT_15.NS": {
        "name": "Nifty Growth Sectors 15",
        "exchange": "NSE",
        "category": "Thematic",
        "sector": "General",
        "description": "15 fastest growing sectors"
    },
    "NIFTY50_EQUAL_WEIGHT.NS": {
        "name": "Nifty 50 Equal Weight",
        "exchange": "NSE",
        "category": "Thematic",
        "sector": "General",
        "description": "Nifty 50 with equal weight to each stock"
    },
    "NIFTY100_QUALTY30.NS": {
        "name": "Nifty Quality 30",
        "exchange": "NSE",
        "category": "Thematic",
        "sector": "General",
        "description": "30 highest quality companies"
    },

    # ===================== STRATEGY / FACTOR =====================
    "NIFTY_ALPHA_30.NS": {
        "name": "Nifty Alpha 30",
        "exchange": "NSE",
        "category": "Strategy",
        "sector": "General",
        "description": "30 stocks with highest alpha"
    },
    "NIFTY50_VALUE_20.NS": {
        "name": "Nifty 50 Value 20",
        "exchange": "NSE",
        "category": "Strategy",
        "sector": "General",
        "description": "Top 20 value stocks from Nifty 50"
    },
    "NIFTY_LOW_VOLATILITY_50.NS": {
        "name": "Nifty Low Volatility 50",
        "exchange": "NSE",
        "category": "Strategy",
        "sector": "General",
        "description": "50 least volatile stocks"
    },
    "NIFTY_MOMENTUM_30.NS": {
        "name": "Nifty Momentum 30",
        "exchange": "NSE",
        "category": "Strategy",
        "sector": "General",
        "description": "30 stocks with highest momentum"
    },
    "NIFTY_HIGH_BETA_50.NS": {
        "name": "Nifty High Beta 50",
        "exchange": "NSE",
        "category": "Strategy",
        "sector": "General",
        "description": "50 highest beta stocks"
    },
    "NIFTY_QUALITY_30.NS": {
        "name": "Nifty Quality 30",
        "exchange": "NSE",
        "category": "Strategy",
        "sector": "General",
        "description": "30 stocks with highest quality score"
    },

    # ===================== VOLATILITY =====================
    "^INDIAVIX": {
        "name": "India VIX",
        "exchange": "NSE",
        "category": "Volatility",
        "sector": "General",
        "description": "India Volatility Index — fear gauge of Indian market"
    },

    # ===================== BSE INDICES =====================
    "^BSESN": {
        "name": "BSE Sensex",
        "exchange": "BSE",
        "category": "Broad Market",
        "sector": "General",
        "description": "Top 30 companies on BSE"
    },
    "BSE-MIDCAP.BO": {
        "name": "BSE Midcap",
        "exchange": "BSE",
        "category": "Broad Market",
        "sector": "General",
        "description": "BSE Midcap index"
    },
    "BSE-SMLCAP.BO": {
        "name": "BSE Smallcap",
        "exchange": "BSE",
        "category": "Broad Market",
        "sector": "General",
        "description": "BSE Smallcap index"
    },
    "^BSE100": {
        "name": "BSE 100",
        "exchange": "BSE",
        "category": "Broad Market",
        "sector": "General",
        "description": "Top 100 companies on BSE"
    },
    "^BSE200": {
        "name": "BSE 200",
        "exchange": "BSE",
        "category": "Broad Market",
        "sector": "General",
        "description": "Top 200 companies on BSE"
    },
    "^BSE500": {
        "name": "BSE 500",
        "exchange": "BSE",
        "category": "Broad Market",
        "sector": "General",
        "description": "Top 500 companies on BSE"
    },
    "S&P_BSE_BANKEX.BO": {
        "name": "BSE Bankex",
        "exchange": "BSE",
        "category": "Sectoral",
        "sector": "Banking",
        "description": "BSE Banking index"
    },
    "S&P_BSE_TECK.BO": {
        "name": "BSE Teck",
        "exchange": "BSE",
        "category": "Sectoral",
        "sector": "IT",
        "description": "BSE Technology index"
    },
    "S&P_BSE_HEALTHCARE.BO": {
        "name": "BSE Healthcare",
        "exchange": "BSE",
        "category": "Sectoral",
        "sector": "Pharma",
        "description": "BSE Healthcare index"
    },
    "S&P_BSE_AUTO.BO": {
        "name": "BSE Auto",
        "exchange": "BSE",
        "category": "Sectoral",
        "sector": "Auto",
        "description": "BSE Auto index"
    },
    "S&P_BSE_METAL.BO": {
        "name": "BSE Metal",
        "exchange": "BSE",
        "category": "Sectoral",
        "sector": "Metals",
        "description": "BSE Metal index"
    },
    "S&P_BSE_OILGAS.BO": {
        "name": "BSE Oil & Gas",
        "exchange": "BSE",
        "category": "Sectoral",
        "sector": "Energy",
        "description": "BSE Oil & Gas index"
    },
    "S&P_BSE_POWER.BO": {
        "name": "BSE Power",
        "exchange": "BSE",
        "category": "Sectoral",
        "sector": "Energy",
        "description": "BSE Power index"
    },
    "S&P_BSE_REALTY.BO": {
        "name": "BSE Realty",
        "exchange": "BSE",
        "category": "Sectoral",
        "sector": "Realty",
        "description": "BSE Realty index"
    },
    "S&P_BSE_IT.BO": {
        "name": "BSE IT",
        "exchange": "BSE",
        "category": "Sectoral",
        "sector": "IT",
        "description": "BSE IT index"
    },
    "S&P_BSE_FMCG.BO": {
        "name": "BSE FMCG",
        "exchange": "BSE",
        "category": "Sectoral",
        "sector": "FMCG",
        "description": "BSE FMCG index"
    },
    "S&P_BSE_CG.BO": {
        "name": "BSE Capital Goods",
        "exchange": "BSE",
        "category": "Sectoral",
        "sector": "Infra",
        "description": "BSE Capital Goods index"
    },
    "S&P_BSE_CONS_DURABLES.BO": {
        "name": "BSE Consumer Durables",
        "exchange": "BSE",
        "category": "Sectoral",
        "sector": "FMCG",
        "description": "BSE Consumer Durables"
    },
    "S&P_BSE_BASICMATERIALS.BO": {
        "name": "BSE Basic Materials",
        "exchange": "BSE",
        "category": "Sectoral",
        "sector": "Metals",
        "description": "BSE Basic Materials"
    },
    "S&P_BSE_INDUSTRIALS.BO": {
        "name": "BSE Industrials",
        "exchange": "BSE",
        "category": "Sectoral",
        "sector": "Infra",
        "description": "BSE Industrials"
    },
}


# ---- Helper: get all symbols as a list ----
def get_all_index_symbols():
    return list(INDIAN_INDICES.keys())


# ---- Helper: get by category ----
def get_indices_by_category(category: str):
    return {k: v for k, v in INDIAN_INDICES.items() if v["category"] == category}


# ---- Helper: get by sector ----
def get_indices_by_sector(sector: str):
    return {k: v for k, v in INDIAN_INDICES.items() if v["sector"] == sector}


# ---- Helper: get by exchange ----
def get_indices_by_exchange(exchange: str):
    return {k: v for k, v in INDIAN_INDICES.items() if v["exchange"] == exchange}


# ---- Categories list ----
CATEGORIES = sorted(set(v["category"] for v in INDIAN_INDICES.values()))
SECTORS = sorted(set(v["sector"] for v in INDIAN_INDICES.values()))
EXCHANGES = sorted(set(v["exchange"] for v in INDIAN_INDICES.values()))