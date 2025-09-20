import pandas as pd

def basic_quality_checks(df: pd.DataFrame) -> list[str]:
    issues: list[str] = []
    required = ["date","country","ticker","currency","price","yield","spread_bps","duration"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        issues.append(f"Missing columns: {missing}")
    if df["yield"].lt(0).any():
        issues.append("Negative yields found")
    if df["spread_bps"].lt(0).any():
        issues.append("Negative spreads found")
    if df["price"].le(0).any():
        issues.append("Non-positive prices found")
    if df.isna().any().any():
        n = int(df.isna().sum().sum())
        issues.append(f"Null values present: {n}")
    return issues
