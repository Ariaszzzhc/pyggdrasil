from flask import Blueprint, request

from ..utils import unsigned_uuid, mongo, bcrypt

account_controller = Blueprint(
    'account_controller',
    __name__,
    url_prefix='/accounts'
)


@account_controller.route('/', methods=['POST'])
def create_account():
    data = request.get_json()
    account = mongo.db.accounts.find_one({'username': data['username']})
    if not account:
        mongo.db.accounts.insert_one({
            "id": unsigned_uuid(data['username']),
            "username": data['username'],
            "password": bcrypt.generate_password_hash(data['password']),
            "profiles": [],
            "properties": []
        })

        return {
            "message": "注册成功"
        }, 200

    else:
        return {
            "error": "Conflict",
            "message": "账户已经存在"
        }, 409
