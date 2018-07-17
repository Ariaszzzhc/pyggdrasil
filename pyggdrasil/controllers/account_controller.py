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
    account = mongo.db.accounts.find_one({'email': data['email']})
    if not account:
        account = {
            "id": unsigned_uuid(data['email']),
            "email": data['email'],
            "accountName": data['accountName'],
            "password": bcrypt.generate_password_hash(data['password']),
            "profiles": [],
            "properties": []
        }

        # TODO 角色的数据结构
        if data['createSameProfile']:
            profile = {
                "id": unsigned_uuid(data['accountName']),
                "name": data['accountName'],
                "model": "default",
                "textures": []
            }

            account["profiles"].append(profile)

        mongo.db.accounts.insert_one(account)

        return {
            "message": "注册成功"
        }, 200

    else:
        return {
            "error": "Conflict",
            "message": "账户已经存在"
        }, 409
