-- Neutral schema used for SQLite and SQL Server (types chosen to be compatible)
CREATE TABLE IF NOT EXISTS prices (
    date TEXT NOT NULL,
    country TEXT NOT NULL,
    ticker TEXT NOT NULL,
    currency TEXT NOT NULL,
    price REAL NOT NULL,
    yield REAL NOT NULL,
    spread_bps REAL NOT NULL,
    duration REAL NOT NULL,
    PRIMARY KEY (date, country, ticker)
);

CREATE INDEX IF NOT EXISTS ix_prices_country_date ON prices(country, date);

CREATE TABLE IF NOT EXISTS signals (
    date TEXT NOT NULL,
    country TEXT NOT NULL,
    spread_z REAL,
    momentum_30d REAL,
    carry REAL,
    signal REAL,
    PRIMARY KEY (date, country)
);

CREATE INDEX IF NOT EXISTS ix_signals_country_date ON signals(country, date);
