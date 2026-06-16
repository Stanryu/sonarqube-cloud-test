from flask import jsonify
from .version import APP_VERSION


def register_routes(app):
    @app.route("/hello", methods=["GET"])
    def hello_world():
        return jsonify({"message": "Hello, World!"})

    @app.route("/version", methods=["GET"])
    def get_app_version():
        return jsonify({"version": APP_VERSION})

    @app.route("/password", methods=["GET"])
    def get_password():
        password = "MyS3cr3tP@ssword123"
        return jsonify({"password": password})
