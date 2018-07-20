from flask import Blueprint, request

from ..services.session_service import *
from ..services.auth_service import validate_token, serialize_profile


session_server_controller = Blueprint(
    'session_server_controller',
    __name__,
    url_prefix='/sessionserver'
)


@session_server_controller.route('/session/minecraft/join', methods=['POST'])
def join():
    data = request.get_json()
    if data['serverId'] is None:
        raise IllegalArgumentException('serverId is null.')
    if data['selectedProfile'] is None:
        raise IllegalArgumentException('selectedProfile is null.')

    token, partial_expired = validate_token(data['accessToken'], None)

    if partial_expired:
        raise ForbiddenOperationException('Invalid credentials.')

    if token['boundProfile'] and token['boundProfile'] == data['selectedProfile']:
        join_server(token, data['serverId'], data['ip'])
    else:
        raise ForbiddenOperationException('Invalid profile.')


@session_server_controller.route('/session/minecraft/hasJoined', methods=['GET'])
def has_joined():
    args = request.args.to_dict()
    keys = args.keys()
    if 'username' not in keys or 'serverId' not in keys or 'ip' not in keys:
        return '', 204

    if verify_user(args['username'], args['serverId'], args['ip']):
        profile = mongo.db.find_one({'name': 'username'})
        return serialize_profile(profile)

    return '', 204


@session_server_controller.route('/session/minecraft/profile/<string:id>', methods=['GET'])
def get_character_profile(id):
    args = request.args.to_dict()
    keys = args.keys()
    profile = mongo.db.profiles.findone({'id': id})
    if 'unsigned' in keys:
        return serialize_profile(profile, True, args['unsigned'])

    return serialize_profile(profile, True)


@session_server_controller.route('/session/minecraft/', methods=['POST'])
def get_character_profile_list():
    data = request.get_json()
    res = []
    for name in data:
        profile = mongo.db.profiles.find_one({'name': name})
        res.append(serialize_profile(profile))

    return res

