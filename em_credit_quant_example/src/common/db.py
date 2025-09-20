from __future__ import annotations
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from .config import settings

_engine: Engine | None = None

def get_engine() -> Engine:
    global _engine
    if _engine is None:
        _engine = create_engine(settings.DATABASE_URL, future=True)
    return _engine

def execute_sql(sql: str) -> None:
    eng = get_engine()
    with eng.begin() as conn:
        conn.execute(text(sql))
