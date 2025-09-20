from __future__ import annotations
from flask.views import MethodView
from src.webapp.services.summary_service import SummaryService


class SummaryAPI(MethodView):
    def __init__(self, service: SummaryService | None = None):
        self.service = service or SummaryService()

    def get(self):
        df = self.service.country_summary()
        return df.to_json(orient="records")