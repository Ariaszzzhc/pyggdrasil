from flask import Blueprint

from ..utils import mongo

auth_server_controller = Blueprint(
    'auth_server_controller',
    __name__,
    url_prefix='/authserver'
)


@auth_server_controller.route('/authenticate', methods=['POST'])
def authenticate():
    pass


@auth_server_controller.route('/refresh', methods=['POST'])
def refresh():
        pass


@auth_server_controller.route('/validate', methods=['POST'])
def validate():
        pass


@auth_server_controller.route('/invalidate', methods=['POST'])
def invalidate():
        pass


@auth_server_controller.route('/signout', methods=['POST'])
def sign_out():
        pass

