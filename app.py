import argparse

from flask import Flask, jsonify, make_response
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

from routes import blueprint

cors = CORS()

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"

SWAGGER_UI_BLUEPRINT = get_swaggerui_blueprint(
    base_url=SWAGGER_URL,
    api_url=API_URL,
    config={
        "api_name": "Flask-REST-Template"
    }
)


def create_app():
    flask_app = Flask(__name__)
    cors.init_app(flask_app)

    # TODO:以下を共通化できるか検討する
    flask_app.register_blueprint(blueprint=SWAGGER_UI_BLUEPRINT, url_prefix=SWAGGER_URL)
    flask_app.register_blueprint(blueprint=blueprint, url_prefix="/")

    # TODO:以下でも可能か検討する
    # flask_app.register_blueprint(book_api.get_blueprint())

    @flask_app.errorhandler(400)
    def handle_400_error(_error):
        """Return a http 400 error to client"""
        return make_response(jsonify({"error": "Misunderstood"}), 400)

    @flask_app.errorhandler(401)
    def handle_401_error(_error):
        """Return a http 401 error to client"""
        return make_response(jsonify({"error": "Unauthorised"}), 401)

    @flask_app.errorhandler(404)
    def handle_404_error(_error):
        """Return a http 404 error to client"""
        return make_response(jsonify({"error": "Not found"}), 404)

    @flask_app.errorhandler(500)
    def handle_500_error(_error):
        """Return a http 500 error to client"""
        return make_response(jsonify({"error": "Server error"}), 500)

    return flask_app


app = create_app()

if __name__ == "__main__":

    PARSER = argparse.ArgumentParser(
        description="Flask-REST-Template")

    PARSER.add_argument("--debug", action="store_true",
                        help="Use flask debug/dev mode with file change reloading")
    ARGS = PARSER.parse_args()

    if ARGS.debug:
        print("Running in debug mode")

        app.run(port=5000, debug=True)
    else:
        app.run(port=5000, debug=False)
