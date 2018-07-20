from flask import Blueprint, request
from ..services.auth_service import mongo, serialize_profile

root_controller = Blueprint(
    'root_controller',
    __name__
)


@root_controller.route('/', methods=['GET'])
def index():
    return "Hello, Minecraft!"


@root_controller.route('/api/profiles/minecraft', methods=['POST'])
def get_profiles():
    data = request.get_json()
    res = []
    for name in data:
        profile = mongo.db.profiles.find_one({'name': name})
        res.append(serialize_profile(profile))

    return res

