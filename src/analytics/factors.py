from __future__ import annotations
import pandas as pd
import numpy as np

def compute_signals(prices: pd.DataFrame) -> pd.DataFrame:
    df = prices.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["country","date"])

    # Spread z-score per country (rolling 120d)
    df["spread_ma"] = df.groupby("country")["spread_bps"].transform(lambda s: s.rolling(120, min_periods=60).mean())
    df["spread_sd"] = df.groupby("country")["spread_bps"].transform(lambda s: s.rolling(120, min_periods=60).std(ddof=0))
    df["spread_z"] = (df["spread_bps"] - df["spread_ma"]) / df["spread_sd"]

    # Momentum: 30d change of spread (tightening positive -> negative spread change)
    df["spread_chg_30d"] = df.groupby("country")["spread_bps"].diff(30)
    df["momentum_30d"] = -df["spread_chg_30d"]  # tighter spreads => positive

    # Carry proxy: yield - 2y US proxy (fixed 4.5% here; replace with risk-free)
    df["carry"] = df["yield"] - 4.5

    # Composite signal (normalized)
    for col in ["spread_z","momentum_30d","carry"]:
        df[col] = df[col].groupby(df["country"]).transform(lambda s: (s - s.mean()) / (s.std(ddof=0) + 1e-9))

    df["signal"] = 0.5*df["momentum_30d"] - 0.3*df["spread_z"] + 0.2*df["carry"]
    out = df[["date","country","spread_z","momentum_30d","carry","signal"]].dropna()
    return out.reset_index(drop=True)
