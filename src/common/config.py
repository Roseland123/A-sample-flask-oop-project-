import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    # Default to local SQLite; swap to SQL Server by setting DATABASE_URL
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///em_credit_quant.db")
    COUNTRIES: tuple[str, ...] = ("BR", "TR", "ZA", "MX")
    START: str = os.getenv("START", "2024-01-01")
    END: str = os.getenv("END", "2025-08-01")
    SEED: int = int(os.getenv("SEED", "42"))

settings = Settings()
