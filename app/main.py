"""
FastAPI backend for the Swedish stock research dashboard.

Scope, on purpose: this app READS market data and your OWN portfolio.
It never places, edits, or cancels an order. See avanza_client.py for why.
"""

import os

import pandas as pd
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from . import avanza_client
from .indicators import build_signal
from .tickers import OMXS30_TICKERS
from .traders import TRADER_CASE_STUDIES

load_dotenv()

app = FastAPI(title="Swedish Stock Research Dashboard", version="0.1.0")

origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok", "demo_mode": avanza_client.DEMO_MODE}


@app.get("/api/portfolio")
def portfolio():
    """Read-only snapshot of your Avanza accounts and holdings."""
    return {
        "overview": avanza_client.get_portfolio_overview(),
        "positions": avanza_client.get_portfolio_positions(),
    }


@app.get("/api/watchlist")
def watchlist():
    """The curated OMXS30 starting universe this app screens."""
    return {"tickers": OMXS30_TICKERS}


@app.get("/api/stock/{ticker}/chart")
def stock_chart(ticker: str, period: str = "one_year"):
    """Historical price series for a ticker, resolved via Avanza search."""
    hits = avanza_client.search_instrument(ticker)
    if not hits:
        raise HTTPException(status_code=404, detail=f"No instrument found for '{ticker}'")

    order_book_id = hits[0]["instrumentId"] if "instrumentId" in hits[0] else hits[0].get("id")
    raw = avanza_client.get_chart_data(order_book_id, period)

    points = raw.get("ohlc") or raw.get("dataPoints") or []
    return {"ticker": ticker, "order_book_id": order_book_id, "points": points}


@app.get("/api/stock/{ticker}/signal")
def stock_signal(ticker: str, period: str = "one_year"):
    """Computed technical signal (SMA/RSI/MACD based) for one ticker."""
    hits = avanza_client.search_instrument(ticker)
    if not hits:
        raise HTTPException(status_code=404, detail=f"No instrument found for '{ticker}'")

    order_book_id = hits[0]["instrumentId"] if "instrumentId" in hits[0] else hits[0].get("id")
    raw = avanza_client.get_chart_data(order_book_id, period)
    points = raw.get("ohlc") or raw.get("dataPoints") or []

    if len(points) < 20:
        raise HTTPException(status_code=422, detail="Not enough history to compute a signal")

    df = pd.DataFrame(points)
    close_col = "close" if "close" in df.columns else "value"
    df = df.rename(columns={close_col: "close"})

    return {"ticker": ticker, "signal": build_signal(df)}


@app.get("/api/traders")
def traders():
    """Educational summaries of well-known historical trades."""
    return {"case_studies": TRADER_CASE_STUDIES}
