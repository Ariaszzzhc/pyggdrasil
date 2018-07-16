import uuid

from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

mongo = PyMongo(app=None)
bcrypt = Bcrypt()


def unsigned_uuid(name):
    class NULL_NAMESPACE:
        bytes = b''

    return str(uuid.uuid3(NULL_NAMESPACE, name)).replace('-', '')
