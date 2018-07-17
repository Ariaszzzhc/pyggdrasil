from ..utils import mongo, bcrypt
from ..exceptions import ForbiddenOperationException


def auth_account(account):
    find_user = mongo.db.accounts.find_one({"name": account['username']})
    if find_user is None:
        raise ForbiddenOperationException("Invalid username or password.")

    if not bcrypt.check_password_hash(find_user['password'], account['password']):
        raise ForbiddenOperationException("Invalid username or password.")

    return find_user
