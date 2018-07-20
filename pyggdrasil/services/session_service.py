import json

from ..exceptions import IllegalArgumentException, ForbiddenOperationException
from ..utils import mongo, redis_store


def join_server(token, server_id, ip=None):
    redis_store.set(server_id, json.dumps([token['accessToken'], token['boundProfile'], ip]), 30)


def verify_user(username, server_id, ip):
    auth = json.loads(redis_store.get(server_id))
    redis_store.delete(server_id)
    if auth is None or auth[2] != ip:
        return False
    profile = mongo.db.profiles.find_one({'id': auth[1]})
    if profile is None or profile['name'] != username:
        return False

    return True
