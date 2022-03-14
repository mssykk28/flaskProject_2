from flask import Blueprint
from flask_restful import Api

from routes.book_api import BookApi, BookDetailApi

blueprint = Blueprint("api", __name__, url_prefix="/")

api = Api()
api.init_app(blueprint)

# TODO:より良い書き方調べる（リソース増えた時どうするか）
api.add_resource(BookApi, "/book")
api.add_resource(BookDetailApi, "/book/<string:book_id>")
