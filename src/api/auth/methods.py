from flask import jsonify
from flask_restful import Resource
from flask_cors import cross_origin
from utils.server import requires_auth, requires_scope


class AuthPublicApi(Resource):
    # This doesn't need authentication
    @cross_origin(headers=["Content-Type", "Authorization"])
    def get(self):
        response = "Hello from a public endpoint! You don't need to be authenticated to see this."
        return jsonify(message=response)


class AuthPrivateApi(Resource):
    # This needs authentication
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self):
        response = "Hello from a private endpoint! You need to be authenticated to see this."
        return jsonify(message=response)


class AuthPrivateScopedApi(Resource):
    # This needs authorization
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self):
        if requires_scope("read:messages"):
            response = "Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this."
            return jsonify(message=response)
        return {
            "code": "Unauthorized",
            "description": "You don't have access to this resource"
        }, 403
