"""
Technical indicators and a simple, transparent, rule-based signal generator.

These are standard, well-known formulas (SMA, EMA, RSI, MACD). Nothing here
predicts the future - it describes the recent shape of a price series so a
human can decide what, if anything, to do about it. Treat every output as
"here is what happened," not "here is what will happen."
"""

import numpy as np
import pandas as pd


def sma(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window, min_periods=window).mean()


def ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()


def rsi(series: pd.Series, window: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def macd(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9):
    fast_ema = ema(series, fast)
    slow_ema = ema(series, slow)
    macd_line = fast_ema - slow_ema
    signal_line = ema(macd_line, signal)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def build_signal(df: pd.DataFrame) -> dict:
    """Given a dataframe with a 'close' column (oldest first), compute
    indicators for the latest point and return a small, explainable signal
    summary. This is a starting point for your own research, not investment
    advice.
    """
    close = df["close"]

    sma20 = sma(close, 20)
    sma50 = sma(close, 50)
    rsi14 = rsi(close, 14)
    macd_line, signal_line, hist = macd(close)

    last = -1
    reasons = []
    score = 0

    if len(close) >= 50 and not pd.isna(sma20.iloc[last]) and not pd.isna(sma50.iloc[last]):
        if sma20.iloc[last] > sma50.iloc[last]:
            score += 1
            reasons.append("20-day average is above the 50-day average (uptrend)")
        else:
            score -= 1
            reasons.append("20-day average is below the 50-day average (downtrend)")

    if not pd.isna(rsi14.iloc[last]):
        r = rsi14.iloc[last]
        if r >= 70:
            score -= 1
            reasons.append(f"RSI at {r:.0f} - historically overbought territory")
        elif r <= 30:
            score += 1
            reasons.append(f"RSI at {r:.0f} - historically oversold territory")

    if not pd.isna(hist.iloc[last]):
        if hist.iloc[last] > 0:
            score += 1
            reasons.append("MACD histogram is positive (momentum leaning up)")
        else:
            score -= 1
            reasons.append("MACD histogram is negative (momentum leaning down)")

    if score >= 2:
        label = "bullish setup"
    elif score <= -2:
        label = "bearish setup"
    else:
        label = "mixed / no clear setup"

    return {
        "label": label,
        "score": score,
        "reasons": reasons,
        "latest_close": float(close.iloc[last]) if len(close) else None,
        "rsi": None if pd.isna(rsi14.iloc[last]) else round(float(rsi14.iloc[last]), 1),
        "sma20": None if pd.isna(sma20.iloc[last]) else round(float(sma20.iloc[last]), 2),
        "sma50": None if pd.isna(sma50.iloc[last]) else round(float(sma50.iloc[last]), 2),
    }
