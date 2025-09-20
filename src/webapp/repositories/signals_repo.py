from __future__ import annotations
import pandas as pd
from sqlalchemy import text
from src.common.db import get_engine


class SignalsRepository:
    def select_signals(self, *, country: str | None) -> pd.DataFrame:
        q = "SELECT date, country, spread_z, momentum_30d, carry, signal FROM signals WHERE 1=1"
        params: dict = {}
        if country:
            q += " AND country = :country"
            params["country"] = country
        q += " ORDER BY date"
        with get_engine().connect() as conn:
            return pd.read_sql(text(q), conn, params=params)