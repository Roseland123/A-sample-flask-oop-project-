from __future__ import annotations
from flask import Flask, jsonify


class ApiError(Exception):
    def __init__(self, message: str, status: int = 400, payload: dict | None = None):
        super().__init__(message)
        self.message = message
        self.status = status
        self.payload = payload or {}


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ApiError)
    def handle_api_error(err: ApiError):
        return jsonify({"error": err.message, **err.payload}), err.status

    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(400)
    def bad_request(_):
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(Exception)
    def internal_error(e):
        app.logger.exception(e)
        return jsonify({"error": "Internal server error"}), 500