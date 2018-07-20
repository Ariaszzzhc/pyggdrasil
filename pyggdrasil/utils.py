import uuid
import json

from flask import Response
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_redis import FlaskRedis

mongo = PyMongo(app=None)
bcrypt = Bcrypt()
redis_store = FlaskRedis()


def unsigned_uuid(name):
    class NULL_NAMESPACE:
        bytes = b''

    return str(uuid.uuid3(NULL_NAMESPACE, name)).replace('-', '')


class JsonResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (list, dict)):
            response = Response(json.dumps(response), mimetype='application/json')
        return super(Response, cls).force_type(response, environ)


def error_message_res(error, error_message, cause=''):
    return {
        "error": error,
        "errorMessage": error_message,
        "cause": cause
    }


def get_server_meta():
    with open('server_meta.json', 'r', encoding='utf-8') as f:
        meta = json.load(f)

    return meta
