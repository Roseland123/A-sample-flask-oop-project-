from __future__ import annotations
from flask import Flask, jsonify, request
from sqlalchemy import text
import pandas as pd
from ..common.db import get_engine
from ..common.config import settings

def create_app() -> Flask:
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    @app.get("/")
    def health():
        return jsonify(status="ok", db=str(settings.DATABASE_URL))

    @app.get("/api/v1/prices")
    def prices():
        country = request.args.get("country")
        date_from = request.args.get("from")
        date_to = request.args.get("to")
        q = "SELECT date, country, ticker, spread_bps, yield, price, duration FROM prices WHERE 1=1"
        params = {}
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
            df = pd.read_sql(text(q), conn, params=params)
        return df.to_json(orient="records", date_format="iso")

    @app.get("/api/v1/signals")
    def signals():
        country = request.args.get("country")
        q = "SELECT date, country, spread_z, momentum_30d, carry, signal FROM signals WHERE 1=1"
        params = {}
        if country:
            q += " AND country = :country"
            params["country"] = country
        q += " ORDER BY date"
        with get_engine().connect() as conn:
            df = pd.read_sql(text(q), conn, params=params)
        return df.to_json(orient="records", date_format="iso")

    @app.get("/api/v1/summary")
    def summary():
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
            df = pd.read_sql(text(q), conn)
        return df.to_json(orient="records")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
