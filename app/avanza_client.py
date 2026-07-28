"""
Read-only wrapper around the unofficial `avanza-api` package.

IMPORTANT SAFETY NOTE
----------------------
This module intentionally exposes only READ operations (overview, positions,
watchlists, search, quotes, chart data). It never imports or calls
`place_order`, `place_stop_loss_order`, `edit_order`, `delete_order`, or any
other endpoint that would move real money or place a real order. If you want
to extend this into an order-placing bot, that is a deliberate, separate
decision you should make with your eyes open - do not casually bolt it on
here.

The underlying library is a reverse-engineered client, not an official
Avanza product. Avanza can change or block the endpoints it uses at any
time, and using it may be against Avanza's terms of service. Use at your
own risk, and never share your username, password, or TOTP secret with
anyone or commit them to source control.
"""

import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()

DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"


class AvanzaUnavailable(Exception):
    """Raised when a real Avanza session can't be established."""


def _mock_overview():
    return {
        "accounts": [
            {
                "accountId": "demo-1",
                "name": "Demo ISK",
                "totalValue": 125430.50,
                "totalProfit": 8120.25,
                "totalProfitPercent": 6.9,
            }
        ]
    }


def _mock_positions():
    return {
        "instrumentPositions": [
            {
                "instrumentType": "STOCK",
                "positions": [
                    {"name": "Volvo B", "ticker": "VOLV-B", "volume": 40,
                     "value": 12400, "averageAcquiredPrice": 285.5,
                     "lastPrice": 310.0},
                    {"name": "Ericsson B", "ticker": "ERIC-B", "volume": 200,
                     "value": 15200, "averageAcquiredPrice": 68.0,
                     "lastPrice": 76.0},
                    {"name": "Investor B", "ticker": "INVE-B", "volume": 60,
                     "value": 18900, "averageAcquiredPrice": 260.0,
                     "lastPrice": 315.0},
                ],
            }
        ]
    }


@lru_cache(maxsize=1)
def _get_client():
    """Create (and cache) a single authenticated Avanza session for the
    process lifetime. Raises AvanzaUnavailable if credentials are missing
    or login fails, so callers can fall back to demo data instead of
    crashing the whole API.
    """
    from avanza import Avanza

    username = os.getenv("AVANZA_USERNAME")
    password = os.getenv("AVANZA_PASSWORD")
    totp_secret = os.getenv("AVANZA_TOTP_SECRET")

    if not (username and password and totp_secret):
        raise AvanzaUnavailable("Avanza credentials are not configured")

    try:
        return Avanza({
            "username": username,
            "password": password,
            "totpSecret": totp_secret,
        })
    except Exception as exc:  # noqa: BLE001 - surface as a clean app error
        raise AvanzaUnavailable(f"Could not log in to Avanza: {exc}") from exc


def get_portfolio_overview() -> dict:
    """Read-only account overview: total value, P/L. Falls back to demo
    data if DEMO_MODE is on or no session can be established."""
    if DEMO_MODE:
        return _mock_overview()
    try:
        return _get_client().get_overview()
    except AvanzaUnavailable:
        return _mock_overview()


def get_portfolio_positions() -> dict:
    """Read-only current holdings across all accounts."""
    if DEMO_MODE:
        return _mock_positions()
    try:
        return _get_client().get_accounts_positions()
    except AvanzaUnavailable:
        return _mock_positions()


def search_instrument(query: str, limit: int = 10):
    """Look up a Swedish stock by name or ticker to find its orderbook id."""
    if DEMO_MODE:
        return []
    return _get_client().search_for_stock(query, limit)


def get_chart_data(order_book_id: str, period: str = "one_year"):
    """Historical OHLC-ish price series for a given orderbook id."""
    from avanza import TimePeriod

    period_map = {
        "one_day": TimePeriod.TODAY if hasattr(TimePeriod, "TODAY") else TimePeriod.ONE_MONTH,
        "one_month": TimePeriod.ONE_MONTH,
        "three_months": TimePeriod.THREE_MONTHS,
        "one_year": TimePeriod.ONE_YEAR,
        "five_years": TimePeriod.FIVE_YEARS,
    }
    return _get_client().get_chart_data(order_book_id, period_map.get(period, TimePeriod.ONE_YEAR))


def get_market_data(order_book_id: str):
    """Current quote / order depth for an instrument."""
    return _get_client().get_market_data(order_book_id)
