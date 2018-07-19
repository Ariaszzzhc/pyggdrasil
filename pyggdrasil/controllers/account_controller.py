from flask import Blueprint, request

from ..services.account_service import *

account_controller = Blueprint(
    'account_controller',
    __name__,
    url_prefix='/accounts'
)


@account_controller.route('/', methods=['POST'])
def create_account():
    data = request.get_json()
    account_data = {
        "email": data['email'],
        "username": data['username'],
        "password": data['password']
    }
    new_account(account_data)

    if data['createSameProfile']:
        new_profile(data['username'], mongo.db.accounts.find_one({"email": data['email']})['id'])

    return {
        "message": "Success"
    }, 200
