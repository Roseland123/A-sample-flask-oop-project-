from __future__ import annotations
from pathlib import Path
import pandas as pd
from ..common.config import settings
from ..common.db import get_engine, execute_sql
from .generate_synth import write_raw_csv
from .validators import basic_quality_checks
from ..analytics.factors import compute_signals

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "db" / "schema.sql"
RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"

def run():
    print("Generating synthetic data...")
    csv_path = write_raw_csv(str(RAW_DIR))

    print("Reading CSV...")
    prices = pd.read_csv(csv_path, parse_dates=["date"])

    print("Running quality checks...")
    issues = basic_quality_checks(prices)
    if issues:
        print("Quality issues detected:")
        for i in issues:
            print(" -", i)
    else:
        print("No issues found.")

    print("Computing signals...")
    signals = compute_signals(prices)

    print("Creating database schema (if needed)...")
    with open(SCHEMA_PATH, "r") as f:
        execute_sql(f.read())

    print("Loading into DB...")
    eng = get_engine()
    prices.to_sql("prices", eng, if_exists="append", index=False)
    signals.to_sql("signals", eng, if_exists="append", index=False)

    print("ETL complete. Rows loaded: prices=%d, signals=%d" % (len(prices), len(signals)))

if __name__ == "__main__":
    run()
