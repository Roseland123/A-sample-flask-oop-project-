from __future__ import annotations
import numpy as np
import pandas as pd
from pathlib import Path
from ..common.config import settings

def generate_daily_em_credit(start: str, end: str, countries: list[str], seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range(start, end, freq="B")
    rows = []
    for c in countries:
        # Base levels per country (spread in bps)
        base_spread = {
            "BR": 280, "TR": 450, "ZA": 320, "MX": 220
        }.get(c, 300)
        base_yield = {
            "BR": 9.5, "TR": 25.0, "ZA": 10.0, "MX": 9.0
        }.get(c, 8.0)
        duration = {
            "BR": 5.5, "TR": 3.0, "ZA": 6.0, "MX": 5.0
        }.get(c, 5.0)
        price = 100.0
        spread = base_spread + rng.normal(0, 5)
        yld = base_yield + rng.normal(0, 0.1)

        for d in dates:
            # random walk with mean reversion
            spread += rng.normal(0, 3) - 0.02*(spread - base_spread)
            yld += rng.normal(0, 0.05) - 0.02*(yld - base_yield)
            price += rng.normal(0, 0.2) - 0.01*(price - 100)

            rows.append({
                "date": d,
                "country": c,
                "ticker": f"{c}GB01",
                "currency": "USD",
                "price": round(price, 4),
                "yield": round(max(yld, 0.0), 4),
                "spread_bps": round(max(spread, 1.0), 2),
                "duration": round(duration + rng.normal(0, 0.05), 3),
            })
    df = pd.DataFrame(rows)
    return df

def write_raw_csv(out_dir: str) -> str:
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    df = generate_daily_em_credit(settings.START, settings.END, list(settings.COUNTRIES), seed=settings.SEED)
    fp = str(Path(out_dir) / "em_credit_prices.csv")
    df.to_csv(fp, index=False)
    return fp
