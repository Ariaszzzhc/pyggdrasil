from flask import Blueprint, request

from ..services.auth_service import *

auth_server_controller = Blueprint(
    'auth_server_controller',
    __name__,
    url_prefix='/authserver'
)


@auth_server_controller.route('/authenticate', methods=['POST'])
def authenticate():
    username = request.json.get('username')
    password = request.json.get('password')
    client_token = request.json.get('clientToken')
    request_user = request.json.get('requestUser')

    if client_token is None:
        client_token = str(uuid.uuid4()).replace('-', '')

    account = validate_password({"username": username, "password": password})
    token = acquire_token(account['id'], client_token)
    profiles = available_profiles(account)

    res = {'accessToken': token['accessToken'],
           'clientToken': token['clientToken'],
           'availableProfiles': [],
           }
    for profile in profiles:
        res['availableProfiles'].append(serialize_profile(profile))

    if token['boundProfile']:
        res['selectedProfile'] = token['boundProfile']

    if request_user:
        res['user'] = serialize_account(account)

    return res


@auth_server_controller.route('/refresh', methods=['POST'])
def refresh():
    access_token = request.json.get('accessToken')
    client_token = request.json.get('clientToken')
    selected_profile = request.json.get('selectedProfile')
    request_user = request.json.get('requestUser')

    token, partial_expired = validate_token(access_token, client_token)

    if selected_profile:
        selected_profile = validate_profile(selected_profile)

        if token['boundProfile']:
            raise IllegalArgumentException("Access token already has a profile assigned.")

        if token['owner'] != selected_profile['owner']:
            raise ForbiddenOperationException("Access denied.")

        new_token = acquire_token(token['owner'], token['clientToken'], selected_profile)

    else:
        new_token = acquire_token(token['owner'], token['clientToken'])

    mongo.db.tokens.delete_one({'accessToken': token['accessToken']})

    res = {
        'accessToken': new_token['accessToken'],
        'clientToken': new_token['clientToken']
    }

    if not token['boundProfile']:
        res['selectedProfile'] = token['boundProfile']

    if request_user:
        res['user'] = serialize_account(mongo.db.accounts.find_one({'id': new_token['owner']}))

    return res


@auth_server_controller.route('/validate', methods=['POST'])
def validate():
    client_token = request.json.get('clientToken')
    access_token = request.json.get('accessToken')
    validate_token(access_token, client_token)
    return '', 204


@auth_server_controller.route('/invalidate', methods=['POST'])
def invalidate():
    access_token = request.json.get('accessToken')
    if access_token is None:
        return '', 204
    token = mongo.db.tokens.find_one({'accessToken': access_token})
    if token is None:
        return '', 204
    mongo.db.tokens.delete_one({'accessToken': token['accessToken']})
    return '', 204


@auth_server_controller.route('/signout', methods=['POST'])
def sign_out():
    username = request.json.get('username')
    password = request.json.get('password')
    account = validate_password({"username": username, "password": password})
    mongo.db.tokens.delete_many({'owner': account['id']})
    return '', 204
