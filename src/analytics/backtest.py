from __future__ import annotations
import pandas as pd
import numpy as np

def toy_pnl(prices: pd.DataFrame, signals: pd.DataFrame) -> pd.DataFrame:
    df = prices.merge(signals, on=["date","country"], how="inner").copy()
    df = df.sort_values(["date","country"])

    # Daily spread return proxy: -Δspread (tightening => positive return)
    df["ret"] = -df.groupby("country")["spread_bps"].diff().fillna(0) / 100.0

    # Positions: normalize by country, cap at +/-1
    pos = df.groupby("country")["signal"].transform(lambda s: s / (s.abs().quantile(0.95) + 1e-9))
    df["position"] = pos.clip(-1, 1)

    df["pnl"] = df["position"] * df["ret"]

    agg = df.groupby("date").agg(
        pnl=("pnl","mean"),
    ).reset_index()
    agg["cum_pnl"] = agg["pnl"].cumsum()
    return agg
