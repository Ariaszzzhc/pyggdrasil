import uuid

from flask import Blueprint, request

from ..utils import error_message_res
from ..services.auth_service import *

auth_server_controller = Blueprint(
    'auth_server_controller',
    __name__,
    url_prefix='/authserver'
)


@auth_server_controller.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    try:
        account = auth_account({"username": data['username'], "password": data['password']})
    except ForbiddenOperationException as e:
        return error_message_res(
            "ForbiddenOperationException",
            e.error_message
        )

    # TODO Token相关


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

