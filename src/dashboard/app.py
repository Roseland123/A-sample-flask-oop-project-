from __future__ import annotations
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from sqlalchemy import text
from ..common.db import get_engine
from ..common.config import settings

def load_prices(country=None):
    q = "SELECT date, country, spread_bps, yield, price FROM prices"
    if country:
        q += " WHERE country = :country"
        with get_engine().connect() as c:
            df = pd.read_sql(text(q), c, params={"country": country})
    else:
        with get_engine().connect() as c:
            df = pd.read_sql(text(q), c)
    df["date"] = pd.to_datetime(df["date"])
    return df

def load_signals(country=None):
    q = "SELECT date, country, spread_z, momentum_30d, carry, signal FROM signals"
    if country:
        q += " WHERE country = :country"
        with get_engine().connect() as c:
            df = pd.read_sql(text(q), c, params={"country": country})
    else:
        with get_engine().connect() as c:
            df = pd.read_sql(text(q), c)
    df["date"] = pd.to_datetime(df["date"])
    return df

def create_dash():
    app = Dash(__name__)
    app.title = "EM Credit Monitor"

    df_prices = load_prices()
    countries = sorted(df_prices["country"].unique()) if not df_prices.empty else []

    app.layout = html.Div([
        html.H2("EM Credit Monitor"),
        html.Div([
            html.Label("Country"),
            dcc.Dropdown(options=[{"label": c, "value": c} for c in countries],
                         value=countries[0] if countries else None,
                         id="country"),
        ], style={"width":"300px"}),
        dcc.Graph(id="spread_chart"),
        dcc.Graph(id="signal_chart"),
    ])

    @app.callback(
        Output("spread_chart", "figure"),
        Input("country", "value"),
    )
    def update_spread(country):
        df = load_prices(country)
        if df.empty:
            return px.line(title="No data")
        return px.line(df, x="date", y="spread_bps", title=f"Spread (bps) - {country}")

    @app.callback(
        Output("signal_chart", "figure"),
        Input("country", "value"),
    )
    def update_signal(country):
        df = load_signals(country)
        if df.empty:
            return px.line(title="No data")
        return px.line(df, x="date", y=["signal","spread_z","momentum_30d","carry"], title=f"Signals - {country}")

    return app

app = create_dash()

if __name__ == "__main__":
    app.run(debug=True)
