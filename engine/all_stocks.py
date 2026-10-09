"""
COMPLETE Indian Stock Database — Every Major NSE/BSE Stock
Organized by sector. Symbol format: TICKER.NS (NSE) or TICKER.BO (BSE)
"""

# ============================================================
#  MAPPING: sector → {symbol: {name, cap_cr}}
#  cap_cr = approximate market cap in ₹ Crores
# ============================================================

def _s(name, cap=10000):
    return {"name": name, "cap": cap}

SECTOR_STOCKS = {

    # ================================================================
    #  BANKING & FINANCE
    # ================================================================
    "Banking": {
        # Private Banks
        "HDFCBANK.NS": _s("HDFC Bank", 1200000),
        "ICICIBANK.NS": _s("ICICI Bank", 700000),
        "KOTAKBANK.NS": _s("Kotak Mahindra Bank", 350000),
        "AXISBANK.NS": _s("Axis Bank", 300000),
        "INDUSINDBK.NS": _s("IndusInd Bank", 80000),
        "FEDERALBNK.NS": _s("Federal Bank", 40000),
        "BANDHANBNK.NS": _s("Bandhan Bank", 30000),
        "IDFCFIRSTB.NS": _s("IDFC First Bank", 40000),
        "RBLBANK.NS": _s("RBL Bank", 15000),
        "CSBBANK.NS": _s("CSB Bank", 8000),
        "DCBBANK.NS": _s("DCB Bank", 6000),
        "KARURVYSYA.NS": _s("Karur Vysya Bank", 10000),
        "SOUTHBANK.NS": _s("Indian Bank", 45000),
        "CITYUNION.NS": _s("City Union Bank", 8000),
        "DHANBANK.NS": _s("Dhanlaxmi Bank", 2000),
        "JKBANK.NS": _s("J&K Bank", 10000),
        "KARNATAKA.NS": _s("Karnataka Bank", 5000),
        "TMBANK.NS": _s("Tamilnad Mercantile Bank", 5000),
        # PSU Banks
        "SBIN.NS": _s("State Bank of India", 500000),
        "BANKBARODA.NS": _s("Bank of Baroda", 120000),
        "PNB.NS": _s("Punjab National Bank", 90000),
        "CANBK.NS": _s("Canara Bank", 70000),
        "UNIONBANK.NS": _s("Union Bank of India", 70000),
        "BANKINDIA.NS": _s("Bank of India", 45000),
        "CENTRALBK.NS": _s("Central Bank of India", 25000),
        "INDIANB.NS": _s("Indian Bank", 45000),
        "UCOBANK.NS": _s("UCO Bank", 25000),
        "IOB.NS": _s("Indian Overseas Bank", 40000),
        "MAHABANK.NS": _s("Bank of Maharashtra", 30000),
        "PSBANK.NS": _s("Punjab & Sind Bank", 10000),
        # Small Finance Banks
        "UJJIVANSFB.NS": _s("Ujjivan Small Finance Bank", 10000),
        "EQUITASBNK.NS": _s("Equitas Small Finance Bank", 8000),
        "SURANASOL.NS": _s("Suryoday Small Finance Bank", 3000),
        "AUROPHARMA.NS": _s("AU Small Finance Bank", 45000),
    },

    "NBFC": {
        "BAJFINANCE.NS": _s("Bajaj Finance", 400000),
        "BAJAJFINSV.NS": _s("Bajaj Finserv", 250000),
        "MUTHOOTFIN.NS": _s("Muthoot Finance", 60000),
        "MANAPPURAM.NS": _s("Manappuram Finance", 18000),
        "SHRIRAMFIN.NS": _s("Shriram Finance", 70000),
        "CHOLAFIN.NS": _s("Cholamandalam Investment", 70000),
        "LICI.NS": _s("Life Insurance Corporation", 500000),
        "SBICARD.NS": _s("SBI Cards", 60000),
        "SBINPS.NS": _s("SBI Payments", 5000),
        "POONAWALLA.NS": _s("Poonawalla Fincorp", 25000),
        "MASFIN.NS": _s("MAS Financial", 3000),
        "APTUS.NS": _s("Aptus Value Housing", 25000),
        "AAVAS.NS": _s("Aavas Financiers", 12000),
        "CANFINHOME.NS": _s("Can Fin Homes", 10000),
        "GRUH.NS": _s("GRUH Finance", 8000),
        "HOMEFIRST.NS": _s("Home First Finance", 10000),
        "PIRAMAL.NS": _s("Piramal Enterprises", 35000),
        "IIFL.NS": _s("IIFL Finance", 15000),
        "L&TFH.NS": _s("L&T Finance Holdings", 30000),
        "RECLTD.NS": _s("REC Limited", 80000),
        "PFC.NS": _s("Power Finance Corp", 90000),
        "IRFC.NS": _s("Indian Railway Finance", 150000),
        "HUDCO.NS": _s("HUDCO", 40000),
        "CDSL.NS": _s("CDSL", 25000),
        "BSE.NS": _s("BSE Limited", 20000),
        "CAMS.NS": _s("CAMS", 15000),
        "KFINTECH.NS": _s("KFin Technologies", 12000),
        "ANGELONE.NS": _s("Angel One", 25000),
        "MOTILALOFS.NS": _s("Motilal Oswal", 35000),
        "IIFL.NS": _s("IIFL Wealth", 12000),
        "JMFINANCIL.NS": _s("JM Financial", 8000),
        "MAHSCOOTER.NS": _s("Maharashtra Scooters", 5000),
        "INDIACEM.NS": _s("India Cements", 8000),
        "PERSISTENT.NS": _s("Persistent Systems", 50000),
    },

    "Insurance": {
        "HDFCLIFE.NS": _s("HDFC Life Insurance", 130000),
        "SBILIFE.NS": _s("SBI Life Insurance", 150000),
        "ICICIPRULI.NS": _s("ICICI Prudential Life", 80000),
        "BAJAJFINSV.NS": _s("Bajaj Allianz Life", 250000),
        "ICICIGI.NS": _s("ICICI Lombard General", 80000),
        "BAJAJHLDNG.NS": _s("Bajaj Holdings", 80000),
        "STARHEALTH.NS": _s("Star Health Insurance", 30000),
        "NEWINDIA.NS": _s("New India Assurance", 25000),
        "NIACL.NS": _s("National Insurance", 15000),
        "ORIENTAL.NS": _s("Oriental Insurance", 10000),
        "UNITED.NS": _s("United India Insurance", 8000),
    },

    # ================================================================
    #  INFORMATION TECHNOLOGY
    # ================================================================
    "IT": {
        "TCS.NS": _s("Tata Consultancy Services", 1200000),
        "INFY.NS": _s("Infosys", 650000),
        "WIPRO.NS": _s("Wipro", 220000),
        "HCLTECH.NS": _s("HCL Technologies", 350000),
        "TECHM.NS": _s("Tech Mahindra", 130000),
        "LTIM.NS": _s("LTIMindtree", 130000),
        "Mphasis.NS": _s("Mphasis", 45000),
        "MPHASIS.NS": _s("Mphasis", 45000),
        "COFORGE.NS": _s("Coforge", 40000),
        "PERSISTENT.NS": _s("Persistent Systems", 50000),
        "LTTS.NS": _s("L&T Technology Services", 45000),
        "KPITTECH.NS": _s("KPIT Technologies", 35000),
        "TATAELXSI.NS": _s("Tata Elxsi", 40000),
        "SONATSOFTW.NS": _s("Sonata Software", 12000),
        "HEXAWARE.NS": _s("Hexaware Technologies", 18000),
        "ZENSAR.NS": _s("Zensar Technologies", 10000),
        "BSOFT.NS": _s("Birlasoft", 12000),
        "MASTEK.NS": _s("Mastek", 7000),
        "NEWGEN.NS": _s("Newgen Software", 10000),
        "NIITTECH.NS": _s("NIIT Technologies", 8000),
        "HAPPSTMNDS.NS": _s("Happiest Minds", 10000),
        "DATAPATTNS.NS": _s("Data Patterns", 10000),
        "ROUTE.NS": _s("Route Mobile", 6000),
        "TANLA.NS": _s("Tanla Platforms", 6000),
        "RATEGAIN.NS": _s("RateGain Travel", 5000),
        "MAPMYINDIA.NS": _s("C.E. Info Systems", 8000),
        "ZOMATO.NS": _s("Zomato", 150000),
        "PAYTM.NS": _s("One97 Communications", 40000),
        "NYKAA.NS": _s("FSN E-Commerce", 50000),
        "DELHIVERY.NS": _s("Delhivery", 35000),
        "POLICYBZR.NS": _s("PB Fintech", 40000),
        "CARTRADE.NS": _s("CarTrade Tech", 5000),
        "IXIGO.NS": _s("Le Travenues Technology", 5000),
    },

    # ================================================================
    #  PHARMA & HEALTHCARE
    # ================================================================
    "Pharma": {
        "SUNPHARMA.NS": _s("Sun Pharma", 300000),
        "DRREDDY.NS": _s("Dr. Reddy's Laboratories", 100000),
        "CIPLA.NS": _s("Cipla", 100000),
        "DIVISLAB.NS": _s("Divi's Laboratories", 120000),
        "AUROPHARMA.NS": _s("Aurobindo Pharma", 50000),
        "LUPIN.NS": _s("Lupin", 50000),
        "TORNTPHARM.NS": _s("Torrent Pharma", 45000),
        "ALKEM.NS": _s("Alkem Laboratories", 60000),
        "BIOCON.NS": _s("Biocon", 35000),
        "MANKIND.NS": _s("Mankind Pharma", 70000),
        "IPCALAB.NS": _s("IPCA Laboratories", 25000),
        "NATCOPHARM.NS": _s("Natco Pharma", 15000),
        "GRANULES.NS": _s("Granules India", 12000),
        "LAURUS.NS": _s("Laurus Labs", 15000),
        "SOLARA.NS": _s("Solara Active Pharma", 3000),
        "AJANTPHARM.NS": _s("Ajanta Pharma", 20000),
        "GLENMARK.NS": _s("Glenmark Pharma", 25000),
        "PFIZER.NS": _s("Pfizer India", 20000),
        "ABBOTINDIA.NS": _s("Abbott India", 45000),
        "GSK.NS": _s("GlaxoSmithKline Pharma", 25000),
        "SANOFI.NS": _s("Sanofi India", 20000),
        "ZYDUSLIFE.NS": _s("Zydus Lifesciences", 70000),
        "JBCHEPHARM.NS": _s("JB Chemicals", 18000),
        "STRIDES.NS": _s("Strides Pharma", 8000),
        "SHOPERSTOP.NS": _s("Shoppers Stop", 8000),
        "METROPOLIS.NS": _s("Metropolis Healthcare", 15000),
        "LALPATHLAB.NS": _s("Dr. Lal PathLabs", 25000),
        "THYROCARE.NS": _s("Thyrocare Technologies", 5000),
        "MAXHEALTH.NS": _s("Max Healthcare", 60000),
        "APOLLOHOSP.NS": _s("Apollo Hospitals", 70000),
        "FORTIS.NS": _s("Fortis Healthcare", 30000),
        "NARAYANHRUD.NS": _s("Narayana Hrudayalaya", 25000),
        "MEDANTA.NS": _s("Global Health (Medanta)", 15000),
        "RAINBOW.NS": _s("Rainbow Children's", 10000),
        "YATHARTH.NS": _s("Yatharth Hospital", 3000),
        "KRISHNADEF.NS": _s("Krishna Institute", 5000),
    },

    # ================================================================
    #  AUTOMOBILE & AUTO ANCILLARY
    # ================================================================
    "Auto": {
        "MARUTI.NS": _s("Maruti Suzuki", 350000),
        "TATAMOTORS.NS": _s("Tata Motors", 250000),
        "M&M.NS": _s("Mahindra & Mahindra", 300000),
        "BAJAJ-AUTO.NS": _s("Bajaj Auto", 200000),
        "HEROMOTOCO.NS": _s("Hero MotoCorp", 80000),
        "EICHERMOT.NS": _s("Eicher Motors", 100000),
        "TVSMOTOR.NS": _s("TVS Motor", 90000),
        "ASHOKLEY.NS": _s("Ashok Leyland", 40000),
        "FORCEMOT.NS": _s("Force Motors", 10000),
        "TIINDIA.NS": _s("T.I. India", 3000),
        "HYUNDAI.NS": _s("Hyundai Motor India", 150000),
        # Auto Ancillary
        "BOSCHLTD.NS": _s("Bosch", 50000),
        "MOTHERSON.NS": _s("Motherson Sumi", 70000),
        "SONACOMS.NS": _s("Sona BLW Precision", 25000),
        "SAMVARDHAN.NS": _s("Samvardhana Motherson", 50000),
        "BALKRISIND.NS": _s("Balkrishna Industries", 30000),
        "MRF.NS": _s("MRF Limited", 50000),
        "APOLLOTYRE.NS": _s("Apollo Tyres", 20000),
        "CEAT.NS": _s("CEAT Limited", 12000),
        "JK.NS": _s("JK Tyre", 10000),
        "GOODYEAR.NS": _s("Goodyear India", 3000),
        "SUNDARMFIN.NS": _s("Sundaram Finance", 35000),
        "SUNDRMFAST.NS": _s("Sundram Fasteners", 12000),
        "BHARATFORG.NS": _s("Bharat Forge", 35000),
        "RAMKRISHNA.NS": _s("Ramkrishna Forgings", 5000),
        "MINDACORP.NS": _s("Minda Corporation", 10000),
        "MOTHERSUMI.NS": _s("Sumi Motherson Wiring", 15000),
        "LUMAX.NS": _s("Lumax Industries", 3000),
        "VARROC.NS": _s("Varroc Engineering", 6000),
        "FIEM.NS": _s("Fiem Industries", 3000),
        "GABRIEL.NS": _s("Gabriel India", 3000),
        "SETCO.NS": _s("Setco Automotive", 1000),
        "SCHAEFFLER.NS": _s("Schaeffler India", 20000),
        "SKF.NS": _s("SKF India", 12000),
        "TIMKEN.NS": _s("Timken India", 8000),
        "NRBBEARING.NS": _s("NRB Bearing", 1000),
        "PRECWIRE.NS": _s("Precision Wires", 2000),
        "AMARARAJA.NS": _s("Amara Raja Energy", 20000),
        "EXIDEIND.NS": _s("Exide Industries", 25000),
        "HBL.NS": _s("HBL Engineering", 3000),
    },

    # ================================================================
    #  FMCG & CONSUMER GOODS
    # ================================================================
    "FMCG": {
        "HINDUNILVR.NS": _s("Hindustan Unilever", 550000),
        "ITC.NS": _s("ITC Limited", 520000),
        "NESTLEIND.NS": _s("Nestle India", 220000),
        "BRITANNIA.NS": _s("Britannia Industries", 120000),
        "TATACONSUM.NS": _s("Tata Consumer Products", 90000),
        "DABUR.NS": _s("Dabur India", 80000),
        "MARICO.NS": _s("Marico Limited", 70000),
        "GODREJCP.NS": _s("Godrej Consumer Products", 100000),
        "COLPAL.NS": _s("Colgate-Palmolive India", 50000),
        "PGHH.NS": _s("Procter & Gamble Health", 40000),
        "EMAMILTD.NS": _s("Emami Limited", 15000),
        "BATA.NS": _s("Bata India", 15000),
        "RELAXO.NS": _s("Relaxo Footwears", 15000),
        "PAGEIND.NS": _s("Page Industries", 40000),
        "UNITDSPR.NS": _s("United Spirits", 75000),
        "RADICO.NS": _s("Radico Khaitan", 20000),
        "UBL.NS": _s("United Breweries", 40000),
        "VSTIND.NS": _s("VST Industries", 8000),
        "GILLETTE.NS": _s("Gillette India", 18000),
        "HONAUT.NS": _s("Honeywell Automation", 30000),
        "PGHL.NS": _s("Procter & Gamble Health", 40000),
        "JYOTHYLAB.NS": _s("Jyothy Labs", 12000),
        "GODREJIND.NS": _s("Godrej Industries", 25000),
        "TASTYBITE.NS": _s("Tasty Bite Eatables", 3000),
        "BIKAJI.NS": _s("Bikaji Foods", 15000),
        "CLEAN.NS": _s("Clean Science", 10000),
        "PRATAAP.NS": _s("Prataap Snacks", 3000),
        "ZYDUS.NS": _s("Zydus Wellness", 10000),
        "CCL.NS": _s("CCL Products", 5000),
        "VADILALIND.NS": _s("Vadilal Industries", 2000),
        "ADFFOODS.NS": _s("ADF Foods", 2000),
        "HERITGFOOD.NS": _s("Heritage Foods", 3000),
        "PARAGMILK.NS": _s("Parag Milk Foods", 1500),
        "HATSUN.NS": _s("Hatsun Agro", 18000),
        "KWALITY.NS": _s("KWALITY", 500),
        "DODLA.NS": _s("Dodla Dairy", 6000),
        "MILKFOOD.NS": _s("Milkfood", 500),
    },

    # ================================================================
    #  ENERGY & OIL AND GAS
    # ================================================================
    "Energy": {
        "RELIANCE.NS": _s("Reliance Industries", 1700000),
        "ONGC.NS": _s("Oil & Natural Gas Corp", 250000),
        "NTPC.NS": _s("NTPC Limited", 300000),
        "POWERGRID.NS": _s("Power Grid Corp", 250000),
        "IOC.NS": _s("Indian Oil Corporation", 180000),
        "BPCL.NS": _s("Bharat Petroleum", 100000),
        "HINDPETRO.NS": _s("Hindustan Petroleum", 80000),
        "GAIL.NS": _s("GAIL India", 80000),
        "OIL.NS": _s("Oil India", 30000),
        "MRPL.NS": _s("MRPL", 15000),
        "CASTROLIND.NS": _s("Castrol India", 15000),
        "PETRONET.NS": _s("Petronet LNG", 30000),
        "IGL.NS": _s("Indraprastha Gas", 25000),
        "MGL.NS": _s("Mahanagar Gas", 12000),
        "GUJGASLTD.NS": _s("Gujarat Gas", 30000),
        "AEGISLOG.NS": _s("Aegis Logistics", 8000),
        "TATAPOWER.NS": _s("Tata Power", 90000),
        "ADANIGREEN.NS": _s("Adani Green Energy", 180000),
        "ADANIPOWER.NS": _s("Adani Power", 200000),
        "ADANITRANS.NS": _s("Adani Energy Solutions", 100000),
        "NHPC.NS": _s("NHPC Limited", 80000),
        "SJVN.NS": _s("SJVN Limited", 30000),
        "TORNTPOWER.NS": _s("Torrent Power", 40000),
        "CESC.NS": _s("CESC Limited", 18000),
        "JSWENERGY.NS": _s("JSW Energy", 50000),
        "RPOWER.NS": _s("Reliance Power", 10000),
        "JPPOWER.NS": _s("Jaiprakash Power", 8000),
        "SUZLON.NS": _s("Suzlon Energy", 60000),
        "INOXGREEN.NS": _s("Inox Green Energy", 8000),
        "RENUKA.NS": _s("Shree Renuka Sugars", 5000),
        "IOC.NS": _s("Indian Oil Corp", 180000),
    },

    # ================================================================
    #  METALS & MINING
    # ================================================================
    "Metals": {
        "TATASTEEL.NS": _s("Tata Steel", 180000),
        "JSWSTEEL.NS": _s("JSW Steel", 200000),
        "HINDALCO.NS": _s("Hindalco Industries", 130000),
        "VEDL.NS": _s("Vedanta Limited", 150000),
        "NATIONALUM.NS": _s("National Aluminium", 25000),
        "HINDZINC.NS": _s("Hindustan Zinc", 130000),
        "NMDC.NS": _s("NMDC Limited", 50000),
        "COALINDIA.NS": _s("Coal India", 150000),
        "SAIL.NS": _s("Steel Authority of India", 50000),
        "JINDALSTEL.NS": _s("Jindal Steel & Power", 50000),
        "JSWENERGY.NS": _s("JSW Energy", 50000),
        "WELCORP.NS": _s("Welspun Corp", 8000),
        "RATNAMANI.NS": _s("Ratnamani Metals", 15000),
        "APLAPOLLO.NS": _s("APL Apollo Tubes", 35000),
        "HINDCOPPER.NS": _s("Hindustan Copper", 8000),
        "JSL.NS": _s("Jindal Stainless", 30000),
        "JSLHISAR.NS": _s("Jindal Stainless Hisar", 15000),
        "BALRAMCHIN.NS": _s("Balrampur Chini", 10000),
        "MAITHANALL.NS": _s("Maithan Alloys", 3000),
        "SHYAMMETL.NS": _s("Shyam Metalics", 12000),
        "RAMCOCEM.NS": _s("Ramco Cements", 20000),
        "GPIL.NS": _s("Godawari Power", 8000),
        "SANDUMA.NS": _s("Sandur Manganese", 3000),
        "MOIL.NS": _s("MOIL Limited", 5000),
        "KIOCL.NS": _s("KIOCL Limited", 5000),
    },

    # ================================================================
    #  REALTY & CONSTRUCTION
    # ================================================================
    "Realty": {
        "DLF.NS": _s("DLF Limited", 180000),
        "GODREJPROP.NS": _s("Godrej Properties", 60000),
        "PRESTIGE.NS": _s("Prestige Estates", 60000),
        "OBEROIRLTY.NS": _s("Oberoi Realty", 60000),
        "BRIGADE.NS": _s("Brigade Enterprises", 25000),
        "PHOENIXLTD.NS": _s("Phoenix Mills", 50000),
        "LODHA.NS": _s("Macrotech Developers", 80000),
        "SUNTV.NS": _s("Sun TV Network", 20000),
        "SOBHA.NS": _s("Sobha Limited", 12000),
        "PREMEXPLQ.NS": _s("Premier Explosives", 3000),
        "SIGNATURE.NS": _s("Signatureglobal", 15000),
        "KOLTEPATIL.NS": _s("Kolte-Patil Developers", 5000),
        "MAHLIFE.NS": _s("Mahindra Lifespace", 5000),
        "PURAVANKARA.NS": _s("Puravankara Limited", 5000),
        "ASHIANA.NS": _s("Ashiana Housing", 2000),
        "AJMERA.NS": _s("Ajmera Realty", 2000),
        "BRIGADE.NS": _s("Brigade Enterprises", 25000),
        "NBCC.NS": _s("NBCC India", 15000),
        "IRCON.NS": _s("Ircon International", 12000),
        "RVNL.NS": _s("Rail Vikas Nigam", 70000),
        "RAILTEL.NS": _s("RailTel Corporation", 10000),
        "CAMPUS.NS": _s("Campus Activewear", 8000),
    },

    # ================================================================
    #  INFRASTRUCTURE & ENGINEERING
    # ================================================================
    "Infra": {
        "LT.NS": _s("Larsen & Toubro", 400000),
        "ADANIENT.NS": _s("Adani Enterprises", 300000),
        "ADANIPORTS.NS": _s("Adani Ports", 250000),
        "SIEMENS.NS": _s("Siemens India", 150000),
        "ABB.NS": _s("ABB India", 100000),
        "BHEL.NS": _s("Bharat Heavy Electricals", 70000),
        "CUMMINSIND.NS": _s("Cummins India", 40000),
        "THERMAX.NS": _s("Thermax Limited", 30000),
        "VOLTAS.NS": _s("Voltas Limited", 30000),
        "BLUESTAR.NS": _s("Blue Star", 30000),
        "HAVELLS.NS": _s("Havells India", 80000),
        "CROMPTON.NS": _s("Crompton Greaves CG", 25000),
        "POLYCAB.NS": _s("Polycab India", 70000),
        "KEI.NS": _s("KEI Industries", 25000),
        "FINOLEX.NS": _s("Finolex Cables", 12000),
        "SUPRAJIT.NS": _s("Suprajit Engineering", 5000),
        "DBCORP.NS": _s("DB Corp", 3000),
        "GRINDWELL.NS": _s("Grindwell Norton", 10000),
        "ELGIEQUIP.NS": _s("Elgi Equipments", 15000),
        "KSB.NS": _s("KSB Limited", 8000),
        "JYOTI.NS": _s("Jyoti Structures", 1000),
        "IRB.NS": _s("IRB Infrastructure", 15000),
        "GRINFRA.NS": _s("GR Infraprojects", 8000),
        "PNC.NS": _s("PNC Infratech", 8000),
        "KNRCON.NS": _s("KNR Constructions", 6000),
        "DILIPBUILDCON.NS": _s("Dilip Buildcon", 5000),
        "HGINFRAST.NS": _s("H.G. Infra Engineering", 5000),
        "RITES.NS": _s("RITES Limited", 12000),
        "ENGINERSIN.NS": _s("Engineers India", 8000),
        "GMRINFRA.NS": _s("GMR Airports Infra", 30000),
    },

    # ================================================================
    #  CEMENT & BUILDING MATERIALS
    # ================================================================
    "Cement": {
        "ULTRACEMCO.NS": _s("UltraTech Cement", 300000),
        "GRASIM.NS": _s("Grasim Industries", 150000),
        "ACC.NS": _s("ACC Limited", 40000),
        "AMBUJACEM.NS": _s("Ambuja Cements", 120000),
        "SHREECEM.NS": _s("Shree Cement", 70000),
        "JKCEMENT.NS": _s("JK Cement", 25000),
        "HEIDELBERG.NS": _s("HeidelbergCement", 12000),
        "RAMCOCEM.NS": _s("Ramco Cements", 20000),
        "DALBHARAT.NS": _s("Dalmia Bharat", 25000),
        "JKLAKSHMI.NS": _s("JK Lakshmi Cement", 8000),
        "NUVOCO.NS": _s("Nuvoco Vistas", 10000),
        "ORIENTCEM.NS": _s("Orient Cement", 5000),
        "STARCEMENT.NS": _s("Star Cement", 5000),
        "INDIACEM.NS": _s("India Cements", 8000),
        "PRISM.NS": _s("Prism Johnson", 5000),
        "SAHYADRI.NS": _s("Sahyadri Industries", 1000),
    },

    # ================================================================
    #  CHEMICALS & FERTILIZERS
    # ================================================================
    "Chemicals": {
        "PIDILITIND.NS": _s("Pidilite Industries", 120000),
        "ASIANPAINT.NS": _s("Asian Paints", 250000),
        "BERGER.NS": _s("Berger Paints", 60000),
        "AKZOINDIA.NS": _s("Akzo Nobel India", 15000),
        "KANSAINER.NS": _s("Kansai Nerolac", 18000),
        "DEEPAKNTR.NS": _s("Deepak Nitrite", 40000),
        "ATUL.NS": _s("Atul Limited", 20000),
        "NAVIN.NS": _s("Navin Fluorine", 15000),
        "SRF.NS": _s("SRF Limited", 70000),
        "FLUOROCHEM.NS": _s("Gujarat Fluorochemicals", 30000),
        "AETHER.NS": _s("Aether Industries", 15000),
        "LXCHEM.NS": _s("Laxmi Organic", 8000),
        "ANURAS.NS": _s("Anupam Rasayan", 8000),
        "CLEAN.NS": _s("Clean Science & Tech", 10000),
        "TATACHEM.NS": _s("Tata Chemicals", 25000),
        "GUJALKALI.NS": _s("Gujarat Alkalies", 5000),
        "DCW.NS": _s("DCW Limited", 2000),
        "GHCL.NS": _s("GHCL Limited", 5000),
        "BASF.NS": _s("BASF India", 15000),
        "DYNAMATECH.NS": _s("Dynamatic Technologies", 5000),
        "UPL.NS": _s("UPL Limited", 35000),
        "PIIND.NS": _s("PI Industries", 50000),
        "BAYERCROP.NS": _s("Bayer CropScience", 20000),
        "SYNGENTA.NS": _s("Syngene International", 25000),
        "RALLIS.NS": _s("Rallis India", 5000),
        "INSECTICID.NS": _s("Insecticides India", 3000),
        "CHAMBLFERT.NS": _s("Chambal Fertilisers", 15000),
        "GSFC.NS": _s("Gujarat State Fertilizers", 8000),
        "NFL.NS": _s("National Fertilizers", 10000),
        "COROMANDEL.NS": _s("Coromandel International", 30000),
        "FACT.NS": _s("Fertilisers & Chemicals", 8000),
        "ZUARI.NS": _s("Zuari Agro Chemicals", 2000),
        "EIDPARRY.NS": _s("EID Parry", 12000),
    },

    # ================================================================
    #  TELECOM & MEDIA
    # ================================================================
    "Telecom": {
        "BHARTIARTL.NS": _s("Bharti Airtel", 480000),
        "IDEA.NS": _s("Vodafone Idea", 50000),
        "INDUS.NS": _s("Indus Towers", 60000),
        "TATACOMM.NS": _s("Tata Communications", 20000),
        "ITI.NS": _s("ITI Limited", 10000),
        "TEJASNET.NS": _s("Tejas Networks", 10000),
        "GTLINFRA.NS": _s("GTL Infrastructure", 2000),
        "ROUTE.NS": _s("Route Mobile", 6000),
        "ONMOBILE.NS": _s("OnMobile Global", 1500),
    },

    "Media": {
        "ZEEL.NS": _s("Zee Entertainment", 15000),
        "SUNTV.NS": _s("Sun TV Network", 20000),
        "PVRINOX.NS": _s("PVR Inox", 15000),
        "DISHTV.NS": _s("Dish TV India", 2000),
        "TVTODAY.NS": _s("TV Today Network", 3000),
        "JAGRAN.NS": _s("Jagran Prakashan", 3000),
        "DBCORP.NS": _s("DB Corp", 3000),
        "NAVNETEDUL.NS": _s("Navneet Education", 3000),
        "NAZARA.NS": _s("Nazara Technologies", 6000),
        "DEN.NS": _s("DEN Networks", 1000),
        "HATHWAY.NS": _s("Hathway Cable", 2000),
    },

    # ================================================================
    #  DEFENSE & AEROSPACE
    # ================================================================
    "Defense": {
        "HAL.NS": _s("Hindustan Aeronautics", 250000),
        "BEL.NS": _s("Bharat Electronics", 180000),
        "BDL.NS": _s("Bharat Dynamics", 50000),
        "SOLARINDS.NS": _s("Solar Industries", 50000),
        "COCHINSHIP.NS": _s("Cochin Shipyard", 40000),
        "GARDENREACH.NS": _s("Garden Reach Shipbuilders", 25000),
        "MAZAGON.NS": _s("Mazagon Dock Shipbuilders", 60000),
        "DATAPATTNS.NS": _s("Data Patterns", 10000),
        "PARAS.NS": _s("Paras Defence", 4000),
        "ZENTEC.NS": _s("Zen Technologies", 5000),
        "APAR.NS": _s("Apar Industries", 25000),
        "CENTUM.NS": _s("Centum Electronics", 3000),
        "DCXINDIA.NS": _s("DCX Systems", 5000),
    },

    # ================================================================
    #  TEXTILES & APPAREL
    # ================================================================
    "Textiles": {
        "PAGEIND.NS": _s("Page Industries", 40000),
        "TRIDENT.NS": _s("Trident Limited", 10000),
        "VARDHMAN.NS": _s("Vardhman Textiles", 10000),
        "ARVIND.NS": _s("Arvind Limited", 5000),
        "SPDL.NS": _s("S.P. Apparels", 2000),
        "KPR.NS": _s("KPR Mill", 8000),
        "WELSPUNIND.NS": _s("Welspun India", 6000),
        "RUCHI.NS": _s("Ruchi Infrastructure", 500),
        "ALOKTEXT.NS": _s("Alok Industries", 3000),
        "SIYARAM.NS": _s("Siyaram Silk Mills", 2000),
        "GRASIM.NS": _s("Grasim (Aditya Birla)", 150000),
        "HIMADRI.NS": _s("Himadri Speciality", 10000),
        "RTNPOWER.NS": _s("RattanIndia Power", 3000),
        "SPANDANA.NS": _s("Spandana Sphoorty", 2000),
    },

    # ================================================================
    #  AGRICULTURE & FOOD PROCESSING
    # ================================================================
    "Agriculture": {
        "EIDPARRY.NS": _s("EID Parry", 12000),
        "BALRAMCHIN.NS": _s("Balrampur Chini", 10000),
        "BANNARIAMM.NS": _s("Bannari Amman Sugars", 3000),
        "RENUKA.NS": _s("Shree Renuka Sugars", 5000),
        "BAJAJHIND.NS": _s("Bajaj Hindusthan", 3000),
        "DCMSHRIRAM.NS": _s("DCM Shriram", 10000),
        "DHAMPUR.NS": _s("Dhampur Sugar Mills", 2000),
        "MAGADSUGAR.NS": _s("Magadh Sugar", 1000),
        "KRBL.NS": _s("KRBL Limited", 5000),
        "LTFOODS.NS": _s("LT Foods", 5000),
        "KOHINOOR.NS": _s("Kohinoor Foods", 500),
        "IBREALEST.NS": _s("Indiabulls Real Estate", 5000),
        "AVANTIFEED.NS": _s("Avanti Feeds", 6000),
        "GODREJAGRO.NS": _s("Godrej Agrovet", 12000),
        "JUBLFOOD.NS": _s("Jubilant Foodworks", 35000),
        "DEVYANI.NS": _s("Devyani International", 18000),
        "SAPPHIRE.NS": _s("Sapphire Foods", 10000),
        "WESTLIFE.NS": _s("Westlife Foodworld", 12000),
        "BECTORFOOD.NS": _s("Mrs. Bectors Food", 5000),
        "VENKEYS.NS": _s("Venky's India", 3000),
        "AWL.NS": _s("Adani Wilmar", 35000),
        "EMAMILTD.NS": _s("Emami", 15000),
    },

    # ================================================================
    #  LOGISTICS & TRANSPORTATION
    # ================================================================
    "Logistics": {
        "DELHIVERY.NS": _s("Delhivery", 35000),
        "CONTAINER.NS": _s("Container Corp", 40000),
        "GATEWAY.NS": _s("Gateway Distriparks", 5000),
        "TCI.NS": _s("TCI Express", 8000),
        "MAHLOG.NS": _s("Mahindra Logistics", 5000),
        "ALLCARGO.NS": _s("Allcargo Logistics", 5000),
        "BLUEDART.NS": _s("Blue Dart Express", 15000),
        "INDIANB.NS": _s("Indian Bank", 45000),
        "SJLOGISTIC.NS": _s("SJ Logistics", 2000),
        "SIS.NS": _s("SIS Limited", 8000),
        "TVSSCS.NS": _s("TVS Supply Chain", 8000),
        "CELLO.NS": _s("Cello World", 15000),
    },

    # ================================================================
    #  CONSUMER DURABLES & ELECTRONICS
    # ================================================================
    "ConsumerDurables": {
        "TITAN.NS": _s("Titan Company", 280000),
        "KAJARIACER.NS": _s("Kajaria Ceramics", 10000),
        "CENTURY.NS": _s("Century Plyboards", 8000),
        "GREENPLY.NS": _s("Greenply Industries", 3000),
        "DIXON.NS": _s("Dixon Technologies", 40000),
        "AMBER.NS": _s("Amber Enterprises", 15000),
        "SYMPHONY.NS": _s("Symphony Limited", 6000),
        "VGUARD.NS": _s("V-Guard Industries", 10000),
        "CROMPTON.NS": _s("Crompton Greaves CG", 25000),
        "WHIRLPOOL.NS": _s("Whirlpool of India", 15000),
        "TTKPRESTIG.NS": _s("TTK Prestige", 10000),
        "BATA.NS": _s("Bata India", 15000),
        "RELAXO.NS": _s("Relaxo Footwears", 15000),
        "RAJESHEXPO.NS": _s("Rajesh Exports", 10000),
        "KALYANKJIL.NS": _s("Kalyan Jewellers", 35000),
        "TITAN.NS": _s("Titan (Tanishq)", 280000),
        "PNGJEWL.NS": _s("PNG Jewellers", 3000),
        "SENCO.NS": _s("Senco Gold", 5000),
        "JCHAC.NS": _s("Johnson Controls", 5000),
        "CERA.NS": _s("Cera Sanitaryware", 5000),
        "HINDWARE.NS": _s("Hindware Home Innovation", 3000),
        "OBEROIRLTY.NS": _s("Oberoi Realty", 60000),
    },

    # ================================================================
    #  PAPER & PACKAGING
    # ================================================================
    "Paper": {
        "JKPAPER.NS": _s("JK Paper", 5000),
        "WESTROST.NS": _s("West Coast Paper", 2000),
        "EMAMIPAP.NS": _s("Emami Paper", 1000),
        "ORIENTPPR.NS": _s("Orient Paper", 1000),
        "SESHAPAPER.NS": _s("Seshasayee Paper", 1000),
        "SATIA.NS": _s("Satia Industries", 500),
        "PAPERPROD.NS": _s("Huhtamaki PPL", 6000),
        "UFPACK.NS": _s("UFlex Limited", 3000),
        "ESABINDIA.NS": _s("Esab India", 8000),
        "ELECON.NS": _s("Elecon Engineering", 8000),
    },

    # ================================================================
    #  MISCELLANEOUS / DIVERSIFIED
    # ================================================================
    "Diversified": {
        "MAHABANK.NS": _s("3M India", 25000),
        "HONAUT.NS": _s("Honeywell Automation", 30000),
        "SCHNEIDER.NS": _s("Schneider Electric", 8000),
        "AAVAS.NS": _s("Aavas Financiers", 12000),
        "MAPMYINDIA.NS": _s("MapmyIndia", 8000),
        "KPITTECH.NS": _s("KPIT Technologies", 35000),
        "ZAGGLE.NS": _s("Zaggle Prepaid", 3000),
        "NETWEB.NS": _s("Netweb Technologies", 10000),
        "KAYNES.NS": _s("Kaynes Technology", 15000),
        "AVALON.NS": _s("Avalon Technologies", 3000),
        "IDEAFORGE.NS": _s("Ideaforge Technology", 5000),
        "ZENTEC.NS": _s("Zen Technologies", 5000),
        "OPTIEMUS.NS": _s("Optiemus Infracom", 3000),
        "RATEGAIN.NS": _s("RateGain Travel", 5000),
        "IXIGO.NS": _s("Le Travenues Technology", 5000),
        "YATRA.NS": _s("Yatra Online", 3000),
        "EASEMYTRIP.NS": _s("Easy Trip Planners", 5000),
    },
}


def get_all_stocks_flat():
    """Return a flat dict: symbol → {name, sector, cap}"""
    flat = {}
    for sector, stocks in SECTOR_STOCKS.items():
        for sym, info in stocks.items():
            if sym not in flat:
                flat[sym] = {"name": info["name"], "sector": sector, "cap": info["cap"]}
    return flat


def get_stock_count():
    return len(get_all_stocks_flat())


def get_sectors():
    return list(SECTOR_STOCKS.keys())


def get_sector_count():
    return {sector: len(stocks) for sector, stocks in SECTOR_STOCKS.items()}