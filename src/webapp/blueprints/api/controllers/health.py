from __future__ import annotations
from flask.views import MethodView
from flask import jsonify
from src.common.config import settings


class HealthAPI(MethodView):
    def get(self):
        return jsonify(status="ok", db=str(settings.DATABASE_URL))