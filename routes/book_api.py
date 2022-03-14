from datetime import datetime, timedelta

import uuid
from flask import jsonify, request, Blueprint
from flask_restful import Resource, abort
from validate_email import validate_email


def get_blueprint():
    """Return the blueprint for the main app module"""
    return Blueprint("book_api", __name__, url_prefix="/book")


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
        return {"id": new_uuid}, 201


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
        return BOOK_REQUESTS[book_id], 200

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
