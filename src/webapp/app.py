from __future__ import annotations
from flask import Flask
from src.webapp.errors import register_error_handlers
from src.webapp.blueprints.api import api_v1_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["JSON_SORT_KEYS"] = False

    # Blueprints
    app.register_blueprint(api_v1_bp)

    # Errors
    register_error_handlers(app)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)