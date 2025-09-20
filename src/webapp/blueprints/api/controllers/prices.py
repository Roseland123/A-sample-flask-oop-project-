from __future__ import annotations
from flask.views import MethodView
from flask import request
from src.webapp.services.prices_service import PricesService


class PricesAPI(MethodView):
    def __init__(self, service: PricesService | None = None):
        self.service = service or PricesService()

    def get(self):
        country = request.args.get("country")
        date_from = request.args.get("from")
        date_to = request.args.get("to")
        df = self.service.fetch_prices(country=country, date_from=date_from, date_to=date_to)
        return df.to_json(orient="records", date_format="iso")