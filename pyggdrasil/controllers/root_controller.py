from flask import Blueprint, request
from ..services.auth_service import mongo, serialize_profile
from ..utils import get_server_meta

root_controller = Blueprint(
    'root_controller',
    __name__
)


@root_controller.route('/', methods=['GET'])
def index():
    meta = get_server_meta()
    with open('public', 'r', encoding='utf-8') as f:
        key_data = f.read()

    meta['signaturePublickey'] = key_data
    return meta


@root_controller.route('/api/profiles/minecraft', methods=['POST'])
def get_profiles():
    data = request.get_json()
    res = []
    for name in data:
        profile = mongo.db.profiles.find_one({'name': name})
        res.append(serialize_profile(profile))

    return res

