from ..exceptions import AlreadyExistException
from ..utils import mongo, unsigned_uuid, bcrypt


def new_account(account_data):
    if mongo.db.accounts.find_one({'email': account_data['email']}) is None:
        mongo.db.accounts.insert_one({
            "id": unsigned_uuid(account_data['email']),
            "email": account_data['email'],
            "username": account_data['username'],
            "password": bcrypt.generate_password_hash(account_data['password']),
            "profiles": []
        })

    else:
        raise AlreadyExistException("Account already exists.")


def new_profile(name, account_id):
    if mongo.db.profiles.find_one({"name": name}) is None:
        profile_id = unsigned_uuid(name)
        mongo.db.profiles.insert_one({
            "id": profile_id,
            "name": name,
            "model": "default",
            "skin": "",
            "cape": "",
            "owner": account_id
        }),

        mongo.db.accounts.update_one({"id": account_id}, {"$addToSet": {"profiles": profile_id}})

    else:
        raise AlreadyExistException("Profile already exists.")
