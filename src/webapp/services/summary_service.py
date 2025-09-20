from __future__ import annotations
import pandas as pd
from src.webapp.repositories.prices_repo import PricesRepository


class SummaryService:
    def __init__(self, repo: PricesRepository | None = None):
        self.repo = repo or PricesRepository()

    def country_summary(self) -> pd.DataFrame:
        return self.repo.country_summary()