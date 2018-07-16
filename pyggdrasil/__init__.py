from flask import Flask

from .config import config_by_name

from .controllers.auth_server_controller import auth_server_controller
from .controllers.account_controller import account_controller
from .controllers.session_server_controller import session_server_controller

from .utils import mongo, bcrypt, JsonResponse


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    app.response_class = JsonResponse

    mongo.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(account_controller)
    # app.register_blueprint(auth_server_controller)
    # app.register_blueprint(session_server_controller)

    return app
