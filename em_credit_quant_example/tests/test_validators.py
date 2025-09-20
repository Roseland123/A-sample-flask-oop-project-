import pandas as pd
from src.etl.validators import basic_quality_checks

def test_quality_checks_pass():
    df = pd.DataFrame({
        "date": ["2025-01-01"],
        "country": ["BR"],
        "ticker": ["BRGB01"],
        "currency": ["USD"],
        "price": [100.0],
        "yield": [9.1],
        "spread_bps": [300.0],
        "duration": [5.0],
    })
    assert basic_quality_checks(df) == []
