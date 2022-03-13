"""A Python Flask REST API BoilerPlate (CRUD) Style"""

import argparse
from datetime import datetime, timedelta

import uuid
from flask import Flask, jsonify, make_response
from flask import request
from flask_cors import CORS
from flask_restful import Resource, abort, Api
from flask_swagger_ui import get_swaggerui_blueprint
from validate_email import validate_email

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

    flask_app.register_blueprint(blueprint=SWAGGER_UI_BLUEPRINT, url_prefix=SWAGGER_URL)

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
api = Api(app)

BOOK_REQUESTS = {
    "8c36e86c-13b9-4102-a44f-646015dfd981": {
        "title": u"Good Book",
        "email": u"testuser1@test.com",
        "timestamp": (datetime.today() - timedelta(1)).timestamp()
    },
    "04cfc704-acb2-40af-a8d3-4611fab54ada": {
        "title": u"Bad Book",
        "email": u"testuser2@test.com",
        "timestamp": (datetime.today() - timedelta(2)).timestamp()
    }
}


@api.resource("/book")
class BookApi(Resource):
    @staticmethod
    def get():
        """Return all book requests
        @return: 200: an array of all known BOOK_REQUESTS as a \
        flask/response object with application/json mimetype.
        """
        return jsonify(BOOK_REQUESTS)

    @staticmethod
    def post():
        """Create a book request record
        @param email: post : the requesters email address
        @param title: post : the title of the book requested
        @return: 201: a new_uuid as a flask/response object \
        with application/json mimetype.
        @raise 400: misunderstood request
        """
        if not request.get_json():
            abort(400)
        data = request.get_json(force=True)

        if not data.get("email"):
            abort(400)
        if not validate_email(data["email"]):
            abort(400)
        if not data.get("title"):
            abort(400)

        new_uuid = str(uuid.uuid4())
        book_request = {
            "title": data["title"],
            "email": data["email"],
            "timestamp": datetime.now().timestamp()
        }
        BOOK_REQUESTS[new_uuid] = book_request
        # HTTP 201 Created
        return jsonify({"id": new_uuid}), 201


@api.resource("/book/<string:book_id>")
class BookDetailApi(Resource):
    @staticmethod
    def get(book_id):
        """Get book request details by its id
        @param book_id: the id
        @return: 200: a BOOK_REQUESTS as a flask/response object \
        with application/json mimetype.
        @raise 404: if book request not found
        """
        if book_id not in BOOK_REQUESTS:
            abort(404)
        return jsonify(BOOK_REQUESTS[book_id])

    @staticmethod
    def put(book_id):
        """Edit a book request record
        @param book_id: the id
        @param email: post : the requesters email address
        @param title: post : the title of the book requested
        @return: 200: a book_request as a flask/response object \
        with application/json mimetype.
        @raise 400: misunderstood request
        """
        if book_id not in BOOK_REQUESTS:
            abort(404)

        if not request.get_json():
            abort(400)
        data = request.get_json(force=True)

        if not data.get("email"):
            abort(400)
        if not validate_email(data["email"]):
            abort(400)
        if not data.get("title"):
            abort(400)

        book_request = {
            "title": data["title"],
            "email": data["email"],
            "timestamp": datetime.now().timestamp()
        }

        BOOK_REQUESTS[book_id] = book_request
        return jsonify(BOOK_REQUESTS[book_id]), 200

    @staticmethod
    def delete(book_id):
        """Delete a book request record
        @param book_id: the id
        @return: 204: an empty payload.
        @raise 404: if book request not found
        """
        if book_id not in BOOK_REQUESTS:
            abort(404)

        del BOOK_REQUESTS[book_id]

        return "", 204


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
