# EM Credit Quant Example (Aug 2025)

An end-to-end **example project** for a Quant Developer/Technologist role:
- **ETL**: ingest → validate → transform → load (SQLite by default; SQL Server optional).
- **Analytics**: factor signals (carry / momentum / z-score), toy PnL/backtest.
- **API**: Flask endpoints for prices, signals, summaries.
- **Dashboard**: Dash/Plotly to interrogate & visualise.
- **OOP**: services, repositories, controllers.
- **CI**: Jenkinsfile skeleton.
- **AI hook**: optional natural-language → SQL helper (no external calls by default).

> Runs entirely offline with synthetic EM credit data (Brazil, Turkey, South Africa, Mexico).


## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 1) Generate synthetic data & load DB
python -m src.etl.pipeline

# 2) Run Flask API
python -m src.api.app

# 3) (optional) Run Dash dashboard (separate terminal)
python -m src.dashboard.app
```

API will listen on http://127.0.0.1:5000  
Dashboard will listen on http://127.0.0.1:8050

### Switch to SQL Server (optional)
1. Uncomment `pyodbc` in `requirements.txt` and install the ODBC driver for SQL Server.
2. Set env var `DATABASE_URL` like:
   - Linux/macOS: `export DATABASE_URL="mssql+pyodbc://USER:PASSWORD@HOST:1433/em_credit_quant?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"`
   - Windows: `set DATABASE_URL=mssql+pyodbc://USER:PASSWORD@HOST:1433/em_credit_quant?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"`
3. Re-run: `python -m src.etl.pipeline`

### Project layout
```
src/
  common/config.py
  common/db.py
  db/schema.sql
  etl/generate_synth.py
  etl/validators.py
  etl/pipeline.py
  analytics/factors.py
  analytics/backtest.py
  api/app.py
  dashboard/app.py
Jenkinsfile
data/raw/ (generated CSVs)
em_credit_quant.db (SQLite after ETL)
```

### Notes
- Replace the DB URL via `DATABASE_URL` when deploying.
- This repo contains **no company names**; safe to include in public portfolios.
