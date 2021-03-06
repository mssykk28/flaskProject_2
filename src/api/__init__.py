from flask import Blueprint
from flask_restful import Api

from src.api.auth.methods import AuthPublicApi, AuthPrivateApi, AuthPrivateScopedApi
from src.api.book.methods import BookApi, BookDetailApi

blueprint = Blueprint("api", __name__, url_prefix="/")

api = Api()
api.init_app(blueprint)

# リソースをrouteを以下のように記述していく
api.add_resource(BookApi, "/book")
api.add_resource(BookDetailApi, "/book/<string:book_id>")
api.add_resource(AuthPublicApi, "/auth/public")
api.add_resource(AuthPrivateApi, "/auth/private")
api.add_resource(AuthPrivateScopedApi, "/auth/privateScoped")
