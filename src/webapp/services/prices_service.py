from __future__ import annotations
import pandas as pd
from src.webapp.repositories.prices_repo import PricesRepository


class PricesService:
    def __init__(self, repo: PricesRepository | None = None):
        self.repo = repo or PricesRepository()

    def fetch_prices(self, *, country: str | None, date_from: str | None, date_to: str | None) -> pd.DataFrame:
        return self.repo.select_prices(country=country, date_from=date_from, date_to=date_to)
