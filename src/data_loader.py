import pandas as pd
import numpy as np
import yfinance as yf
import pandas_datareader.data as web

from utils import (
    RAW_DIR, PROCESSED_DIR, UNIVERSE_FILE,
    START_DATE, END_DATE, ensure_dirs,
)


# ── Universe ───────────────────────────────────────────────────────────────────

def load_universe() -> list[str]:
    df = pd.read_csv(UNIVERSE_FILE)
    tickers = df["ticker"].str.strip().tolist()
    print(f"[data_loader] Universe: {len(tickers)} tickers")
    return tickers


# ── Price data ─────────────────────────────────────────────────────────────────

def download_prices(tickers: list[str],
                    start: str = START_DATE,
                    end: str = END_DATE) -> pd.DataFrame:
    raw = yf.download(tickers, start=start, end=end, auto_adjust=True)

    if isinstance(raw.columns, pd.MultiIndex):
        prices = raw["Close"]
    else:
        prices = raw[["Close"]]
        prices.columns = tickers

    prices = prices.dropna(how="all")
    prices.to_csv(RAW_DIR / "daily_prices.csv")
    return prices


def compute_monthly_returns(prices: pd.DataFrame) -> pd.DataFrame:
    monthly_prices = prices.resample("ME").last()
    monthly_returns = monthly_prices.pct_change().dropna(how="all")
    monthly_returns.to_csv(PROCESSED_DIR / "monthly_returns.csv")
    return monthly_returns


# ── Fama-French factors ───────────────────────────────────────────────────────

def load_ff3_factors() -> pd.DataFrame:
    ff = web.DataReader("F-F_Research_Data_Factors", "famafrench", start=START_DATE, end=END_DATE)
    ff3 = ff[0] / 100.0
    ff3.index = ff3.index.to_timestamp("M")
    ff3.to_csv(RAW_DIR / "ff3_factors.csv")
    return ff3


def load_all_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    ensure_dirs()
    tickers = load_universe()
    prices = download_prices(tickers)
    monthly_returns = compute_monthly_returns(prices)
    ff3 = load_ff3_factors()
    return prices, monthly_returns, ff3