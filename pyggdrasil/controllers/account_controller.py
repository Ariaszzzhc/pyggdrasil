from flask import Blueprint, request

from ..services.account_service import *

account_controller = Blueprint(
    'account_controller',
    __name__,
    url_prefix='/accounts'
)


@account_controller.route('/', methods=['POST'])
def create_account():
    create_same_profile = request.json.get('createSameProfile')
    account_data = {
        "email": request.json.get('email'),
        "username": request.json.get('username'),
        "password": request.json.get('password')
    }
    new_account(account_data)

    if create_same_profile:
        new_profile(request.json.get('username'),
                    mongo.db.accounts.find_one({"email": request.json.get('email')})['id'])

    return {
               "message": "Success"
           }, 200
