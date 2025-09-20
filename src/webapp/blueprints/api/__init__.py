# src/webapp/blueprints/api/__init__.py
from __future__ import annotations
from flask import Blueprint
from .controllers.health import HealthAPI
from .controllers.prices import PricesAPI
from .controllers.signals import SignalsAPI
from .controllers.summary import SummaryAPI

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/")

# Health at root
api_v1_bp.add_url_rule("", view_func=HealthAPI.as_view("health"), methods=["GET"])

# /api/v1/*
api_prefix = "/api/v1"
api_v1_bp.add_url_rule(f"{api_prefix}/prices",  view_func=PricesAPI.as_view("prices"),  methods=["GET"])
api_v1_bp.add_url_rule(f"{api_prefix}/signals", view_func=SignalsAPI.as_view("signals"), methods=["GET"])
api_v1_bp.add_url_rule(f"{api_prefix}/summary", view_func=SummaryAPI.as_view("summary"), methods=["GET"])
