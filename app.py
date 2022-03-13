"""A Python Flask REST API BoilerPlate (CRUD) Style"""

import argparse

from flask import Flask, jsonify, make_response
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from routes import book_api

api = Flask(__name__)

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"

SWAGGER_UI_BLUEPRINT = get_swaggerui_blueprint(
    base_url=SWAGGER_URL,
    api_url=API_URL,
    config={
        "api_name": "Flask-REST-Boilerplate"
    }
)
api.register_blueprint(blueprint=SWAGGER_UI_BLUEPRINT, url_prefix=SWAGGER_URL)

api.register_blueprint(blueprint=book_api.get_blueprint())


@api.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({"error": "Misunderstood"}), 400)


@api.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({"error": "Unauthorised"}), 401)


@api.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({"error": "Not found"}), 404)


@api.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({"error": "Server error"}), 500)


if __name__ == "__main__":

    PARSER = argparse.ArgumentParser(
        description="Flask-REST-Template")

    PARSER.add_argument("--debug", action="store_true",
                        help="Use flask debug/dev mode with file change reloading")
    ARGS = PARSER.parse_args()

    if ARGS.debug:
        print("Running in debug mode")
        CORS = CORS(api)
        api.run(port=5000, debug=True)
    else:
        api.run(port=5000, debug=False)
