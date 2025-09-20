from __future__ import annotations
from flask.views import MethodView
from flask import request
from src.webapp.services.signals_service import SignalsService


class SignalsAPI(MethodView):
    def __init__(self, service: SignalsService | None = None):
        self.service = service or SignalsService()

    def get(self):
        country = request.args.get("country")
        df = self.service.fetch_signals(country=country)
        return df.to_json(orient="records", date_format="iso")