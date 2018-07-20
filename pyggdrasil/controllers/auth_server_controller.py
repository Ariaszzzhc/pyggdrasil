from flask import Blueprint, request

from ..services.auth_service import *

auth_server_controller = Blueprint(
    'auth_server_controller',
    __name__,
    url_prefix='/authserver'
)


@auth_server_controller.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.get_json()
    if data['clientToken'] is None:
        data['clientToken'] = str(uuid.uuid4()).replace('-', '')
    account = validate_password({"username": data['username'], "password": data['password']})
    account.pop('_id')
    token = acquire_token(account['id'], data['clientToken'])
    profiles = available_profiles(account)

    res = {'accessToken': token['accessToken'],
           'clientToken': token['clientToken'],
           'availableProfiles': [],
           }
    for profile in profiles:
        res['availableProfiles'].append(serialize_profile(profile))

    if token['boundProfile']:
        res['selectedProfile'] = token['boundProfile']

    if data['requestUser']:
        res['user'] = serialize_account(account)

    return res


@auth_server_controller.route('/refresh', methods=['POST'])
def refresh():
    data = request.get_json()
    token, partial_expired = validate_token(data['accessToken'], data['clientToken'])

    if data['selectedProfile']:
        selected_profile = validate_profile(data['selectedProfile'])

        if not token['boundProfile'] is None:
            raise IllegalArgumentException("Access token already has a profile assigned.")

        if token['owner'] != selected_profile['owner']:
            raise ForbiddenOperationException("Access denied.")

        new_token = acquire_token(token['owner'], token['clientToken'], data['selectedProfile'])

    else:
        new_token = acquire_token(token['owner'], token['clientToken'])

    mongo.db.tokens.delete_one({'accessToken': token['accessToken']})

    res = {
        'accessToken': new_token['accessToken'],
        'clientToken': new_token['clientToken']
    }

    if not token['boundProfile']:
        res['selectedProfile'] = token['boundProfile']

    if data['requestUser']:
        res['user'] = serialize_account(mongo.db.accounts.find_one({'id': new_token['owner']}))

    return res


@auth_server_controller.route('/validate', methods=['POST'])
def validate():
    data = request.get_json()
    validate_token(data['accessToken'], data['clientToken'])
    return '', 204


@auth_server_controller.route('/invalidate', methods=['POST'])
def invalidate():
    data = request.get_json()
    token, partial_expired = validate_token(data['accessToken'], data['clientToken'])
    mongo.db.tokens.delete_one({'accessToken': token['accessToken']})
    return '', 204


@auth_server_controller.route('/signout', methods=['POST'])
def sign_out():
    data = request.get_json()
    account = validate_password({"username": data['username'], "password": data['password']})
    mongo.db.tokens.delete_many({'owner': account['id']})
    return '', 204

