from __future__ import annotations
import pandas as pd
from sqlalchemy import text
from src.common.db import get_engine


class PricesRepository:
    def select_prices(self, *, country: str | None, date_from: str | None, date_to: str | None) -> pd.DataFrame:
        q = "SELECT date, country, ticker, spread_bps, yield, price, duration FROM prices WHERE 1=1"
        params: dict = {}
        if country:
            q += " AND country = :country"
            params["country"] = country
        if date_from:
            q += " AND date >= :date_from"
            params["date_from"] = date_from
        if date_to:
            q += " AND date <= :date_to"
            params["date_to"] = date_to
        q += " ORDER BY date"
        with get_engine().connect() as conn:
            return pd.read_sql(text(q), conn, params=params)

    def country_summary(self) -> pd.DataFrame:
        q = (
            "SELECT country, "
            "COUNT(*) as n, "
            "AVG(spread_bps) as avg_spread_bps, "
            "AVG(yield) as avg_yield, "
            "AVG(duration) as avg_duration "
            "FROM prices "
            "GROUP BY country "
            "ORDER BY country"
        )
        with get_engine().connect() as conn:
            return pd.read_sql(text(q), conn)