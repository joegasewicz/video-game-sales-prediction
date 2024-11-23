from flask import Flask

api = Flask(__name__, static_folder="static")


def create_app() -> Flask:
    from web_api.home_view import home_view
    api.register_blueprint(home_view)
    return api

