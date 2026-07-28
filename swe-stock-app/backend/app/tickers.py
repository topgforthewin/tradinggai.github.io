"""
A small curated starting list of large, liquid Stockholm exchange (OMXS30)
companies. Avanza's orderbook ids differ per share class and aren't stable
across environments, so at startup the app resolves each ticker to its real
orderbook id via search_for_stock() rather than hardcoding ids that could go
stale. Extend this list freely - it's just a starting universe, not "all"
Swedish companies (there are ~900 listed across all lists; add more tickers
here or wire up a fuller instrument-list endpoint if you want full coverage).
"""

OMXS30_TICKERS = [
    {"ticker": "ERIC-B", "name": "Ericsson B"},
    {"ticker": "VOLV-B", "name": "Volvo B"},
    {"ticker": "INVE-B", "name": "Investor B"},
    {"ticker": "ATCO-A", "name": "Atlas Copco A"},
    {"ticker": "ATCO-B", "name": "Atlas Copco B"},
    {"ticker": "SAND", "name": "Sandvik"},
    {"ticker": "SEB-A", "name": "SEB A"},
    {"ticker": "SHB-A", "name": "Handelsbanken A"},
    {"ticker": "SWED-A", "name": "Swedbank A"},
    {"ticker": "HM-B", "name": "H&M B"},
    {"ticker": "ASSA-B", "name": "Assa Abloy B"},
    {"ticker": "ALFA", "name": "Alfa Laval"},
    {"ticker": "SKF-B", "name": "SKF B"},
    {"ticker": "TELIA", "name": "Telia"},
    {"ticker": "ESSITY-B", "name": "Essity B"},
    {"ticker": "HEXA-B", "name": "Hexagon B"},
    {"ticker": "EVO", "name": "Evolution"},
    {"ticker": "SCA-B", "name": "SCA B"},
    {"ticker": "AZN", "name": "AstraZeneca"},
    {"ticker": "BOL", "name": "Boliden"},
    {"ticker": "EQT", "name": "EQT"},
    {"ticker": "GETI-B", "name": "Getinge B"},
    {"ticker": "KINV-B", "name": "Kinnevik B"},
    {"ticker": "NDA-SE", "name": "Nordea"},
    {"ticker": "NIBE-B", "name": "NIBE Industrier B"},
    {"ticker": "SBB-B", "name": "SBB B"},
    {"ticker": "SINCH", "name": "Sinch"},
    {"ticker": "TEL2-B", "name": "Tele2 B"},
    {"ticker": "LATO-B", "name": "Latour B"},
    {"ticker": "SAAB-B", "name": "Saab B"},
]
