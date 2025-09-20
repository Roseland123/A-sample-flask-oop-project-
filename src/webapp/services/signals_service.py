from __future__ import annotations
import pandas as pd
from src.webapp.repositories.signals_repo import SignalsRepository


class SignalsService:
    def __init__(self, repo: SignalsRepository | None = None):
        self.repo = repo or SignalsRepository()

    def fetch_signals(self, *, country: str | None) -> pd.DataFrame:
        return self.repo.select_signals(country=country)